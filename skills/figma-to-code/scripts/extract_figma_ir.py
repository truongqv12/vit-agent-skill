#!/usr/bin/env python3
"""
Normalize a figma-mcp-go style JSON dump into a smaller implementation IR.

Goals:
- keep only one selected target frame/component/instance subtree
- remove hidden, opacity-zero, off-canvas, and unrelated sibling nodes
- classify semantic UI roles such as modal/header/footer/field/button/icon
- summarize tokens/layout so the coding agent does not need to read raw output

Usage:
  python extract_figma_ir.py --input raw-output.json --out figma-ir.json --target-node-id 5675:288345
  python extract_figma_ir.py --input raw-output.json --out figma-ir.json
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

Node = Dict[str, Any]

CONTAINER_TYPES = {"FRAME", "GROUP", "COMPONENT", "COMPONENT_SET", "INSTANCE", "SECTION"}
VISIBLE_TYPES = CONTAINER_TYPES | {"TEXT", "VECTOR", "RECTANGLE", "ELLIPSE", "LINE", "POLYGON", "STAR", "BOOLEAN_OPERATION"}

ROLE_PATTERNS = [
    ("close-button", re.compile(r"close|dismiss|x$|đóng", re.I)),
    ("chevron-icon", re.compile(r"chevron|caret|arrow[-_ ]?down", re.I)),
    ("calendar-icon", re.compile(r"calendar|date|ngày", re.I)),
    ("upload-icon", re.compile(r"upload|tải", re.I)),
    ("image-placeholder", re.compile(r"image|ảnh|avatar|logo", re.I)),
]

TEXT_SECTION_RE = re.compile(r"^[A-ZÀ-Ỹ0-9 &/\-]{3,}$")


def configure_stdio() -> None:
    """Make Windows console output safer for Vietnamese text."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def read_json(path: str | Path) -> Any:
    """Read JSON exported by Figma/MCP safely on Windows.

    utf-8-sig handles both normal UTF-8 and UTF-8 with BOM.
    Do not use json.load(open(path)) without encoding on Windows.
    """
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def union_bounds(nodes: List[Node]) -> Optional[Dict[str, float]]:
    boxes = [bounds(n) for n in nodes if isinstance(n, dict) and bounds(n)]
    boxes = [b for b in boxes if b]
    if not boxes:
        return None
    min_x = min(b["x"] for b in boxes)
    min_y = min(b["y"] for b in boxes)
    max_x = max(b["x"] + b["width"] for b in boxes)
    max_y = max(b["y"] + b["height"] for b in boxes)
    return {"x": min_x, "y": min_y, "width": max_x - min_x, "height": max_y - min_y}


def unwrap_mcp_payload(data: Any) -> Node:
    """Normalize common MCP response wrappers into a node-like root.

    figma-mcp-go tools can return either a direct node tree or a wrapper like
    {"context": [node, ...]}. The extractor should support both so agents do
    not write ad-hoc `python -c json.load(open(...))` inspections.
    """
    if not isinstance(data, dict):
        raise SystemExit("input JSON must be an object")

    if isinstance(data.get("context"), list):
        context = [n for n in data["context"] if isinstance(n, dict)]
        if len(context) == 1:
            return context[0]
        if context:
            return {
                "id": "mcp-context-root",
                "name": "MCP context root",
                "type": "FRAME",
                "bounds": union_bounds(context) or {"x": 0, "y": 0, "width": 0, "height": 0},
                "children": context,
            }

    # Some tools wrap the useful node under these keys.
    for key in ("node", "document", "result", "data"):
        value = data.get(key)
        if isinstance(value, dict) and ("type" in value or "children" in value):
            return value

    # Figma REST `/files/:key/nodes` shape: {"nodes": {"id": {"document": ...}}}
    nodes = data.get("nodes")
    if isinstance(nodes, dict):
        documents = []
        for value in nodes.values():
            if isinstance(value, dict):
                doc = value.get("document")
                if isinstance(doc, dict):
                    documents.append(doc)
        if len(documents) == 1:
            return documents[0]
        if documents:
            return {
                "id": "figma-rest-nodes-root",
                "name": "Figma REST nodes root",
                "type": "FRAME",
                "bounds": union_bounds(documents) or {"x": 0, "y": 0, "width": 0, "height": 0},
                "children": documents,
            }

    return data


def bounds(node: Node) -> Optional[Dict[str, float]]:
    b = node.get("bounds") or node.get("absoluteBoundingBox")
    if not isinstance(b, dict):
        return None
    try:
        return {
            "x": float(b.get("x", 0)),
            "y": float(b.get("y", 0)),
            "width": float(b.get("width", 0)),
            "height": float(b.get("height", 0)),
        }
    except (TypeError, ValueError):
        return None


def area(node: Node) -> float:
    b = bounds(node)
    if not b:
        return 0.0
    return max(0.0, b["width"]) * max(0.0, b["height"])


def intersects(a: Dict[str, float], b: Dict[str, float], tolerance: float = 1.0) -> bool:
    return not (
        a["x"] + a["width"] < b["x"] - tolerance
        or b["x"] + b["width"] < a["x"] - tolerance
        or a["y"] + a["height"] < b["y"] - tolerance
        or b["y"] + b["height"] < a["y"] - tolerance
    )


def contains(outer: Dict[str, float], inner: Dict[str, float], tolerance: float = 2.0) -> bool:
    return (
        inner["x"] >= outer["x"] - tolerance
        and inner["y"] >= outer["y"] - tolerance
        and inner["x"] + inner["width"] <= outer["x"] + outer["width"] + tolerance
        and inner["y"] + inner["height"] <= outer["y"] + outer["height"] + tolerance
    )


def walk(node: Node, ancestors: Optional[List[Node]] = None) -> Iterable[Tuple[Node, List[Node]]]:
    ancestors = ancestors or []
    yield node, ancestors
    for child in node.get("children") or []:
        if isinstance(child, dict):
            yield from walk(child, ancestors + [node])


def find_by_id(root: Node, node_id: str) -> Optional[Node]:
    for node, _ in walk(root):
        if node.get("id") == node_id:
            return node
    return None


def choose_target(root: Node) -> Node:
    candidates = []
    for node, ancestors in walk(root):
        t = node.get("type")
        b = bounds(node)
        if t in CONTAINER_TYPES and b and b["width"] >= 120 and b["height"] >= 80:
            name = str(node.get("name") or "")
            score = area(node)
            if any(word in name.lower() for word in ["popup", "modal", "dialog", "screen", "page", "frame"]):
                score *= 1.25
            # Penalize document-size roots containing unrelated off-canvas screens.
            if len(node.get("children") or []) > 80:
                score *= 0.8
            candidates.append((score, node))
    if not candidates:
        return root
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def effective_visible(node: Node, ancestors: List[Node]) -> bool:
    for n in ancestors + [node]:
        if n.get("visible") is False:
            return False
        try:
            if float(n.get("opacity", 1)) == 0:
                return False
        except (TypeError, ValueError):
            pass
    return True


def normalize_styles(styles: Any) -> Dict[str, Any]:
    if not isinstance(styles, dict):
        return {}
    out: Dict[str, Any] = {}
    for key in [
        "fills",
        "strokes",
        "fontFamily",
        "fontSize",
        "fontStyle",
        "fontWeight",
        "lineHeight",
        "textAlignHorizontal",
        "effects",
        "cornerRadius",
        "strokeWeight",
    ]:
        if key in styles:
            out[key] = styles[key]
    return out


def classify_role(node: Node, target_bounds: Optional[Dict[str, float]]) -> str:
    name = str(node.get("name") or "")
    node_type = node.get("type")
    text = str(node.get("characters") or "")
    b = bounds(node)

    for role, pattern in ROLE_PATTERNS:
        if pattern.search(name) or pattern.search(text):
            return role

    if node_type == "TEXT":
        if TEXT_SECTION_RE.match(text.strip()) and len(text.strip()) <= 40:
            return "section-title"
        if text.strip().endswith("*") or (b and b["height"] <= 22 and len(text) <= 80):
            return "text"
        return "text"

    if b:
        # Common input dimensions in enterprise forms.
        if 28 <= b["height"] <= 52 and b["width"] >= 120 and node_type in {"VECTOR", "RECTANGLE"}:
            return "control-box"
        if target_bounds and b["width"] >= target_bounds["width"] * 0.85 and b["height"] <= 2:
            return "divider"
        if 24 <= b["height"] <= 48 and 40 <= b["width"] <= 180:
            return "button-bg"
        if b["width"] <= 32 and b["height"] <= 32:
            return "icon"

    return "container" if node_type in CONTAINER_TYPES else "shape"


def collect_tokens(nodes: List[Node]) -> Dict[str, Any]:
    colors = Counter()
    fonts = Counter()
    font_sizes = Counter()
    font_weights = Counter()
    radii = Counter()
    strokes = Counter()

    for n in nodes:
        st = normalize_styles(n.get("styles"))
        for key in ["fills", "strokes"]:
            value = st.get(key)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        colors[item] += 1
            elif isinstance(value, str):
                colors[value] += 1
        if st.get("fontFamily"):
            fonts[str(st["fontFamily"])] += 1
        if st.get("fontSize") is not None:
            font_sizes[str(st["fontSize"])] += 1
        if st.get("fontWeight") is not None:
            font_weights[str(st["fontWeight"])] += 1
        if st.get("cornerRadius") is not None:
            radii[str(st["cornerRadius"])] += 1
        if st.get("strokeWeight") is not None:
            strokes[str(st["strokeWeight"])] += 1

    return {
        "colors": colors.most_common(20),
        "fonts": fonts.most_common(10),
        "fontSizes": font_sizes.most_common(12),
        "fontWeights": font_weights.most_common(10),
        "radii": radii.most_common(10),
        "strokeWeights": strokes.most_common(10),
    }


def cluster_positions(values: List[float], tolerance: float = 6.0) -> List[float]:
    if not values:
        return []
    values = sorted(values)
    clusters: List[List[float]] = [[values[0]]]
    for value in values[1:]:
        if abs(value - sum(clusters[-1]) / len(clusters[-1])) <= tolerance:
            clusters[-1].append(value)
        else:
            clusters.append([value])
    return [round(sum(c) / len(c), 2) for c in clusters]


def infer_layout(semantic_nodes: List[Node], target_bounds: Dict[str, float]) -> Dict[str, Any]:
    text_nodes = [n for n in semantic_nodes if n.get("type") == "TEXT" and bounds(n)]
    box_nodes = [n for n in semantic_nodes if n.get("role") in {"control-box", "button-bg"} and bounds(n)]

    xs = [bounds(n)["x"] for n in box_nodes if bounds(n)]
    widths = [bounds(n)["width"] for n in box_nodes if bounds(n)]
    ys = [bounds(n)["y"] for n in semantic_nodes if bounds(n)]

    columns = cluster_positions(xs, tolerance=8)
    rows = cluster_positions(ys, tolerance=4)

    sections = []
    for n in text_nodes:
        if n.get("role") == "section-title":
            b = bounds(n)
            sections.append({"text": n.get("characters"), "y": b["y"], "x": b["x"]})

    return {
        "target": target_bounds,
        "columns": columns,
        "commonControlWidths": Counter(round(w) for w in widths).most_common(8),
        "rowYClusters": rows[:80],
        "sections": sections,
    }


def effective_target_bounds(target: Node) -> Optional[Dict[str, float]]:
    """Return bounds used for clipping.

    Some MCP/plugin serializers return the selected FRAME bounds in absolute
    canvas coordinates while its children are normalized to a local 0,0 space.
    When that happens, use a same-size background child or children extent as
    the clipping box so visible children are not dropped as off-canvas.
    """
    tb = bounds(target)
    children = [c for c in (target.get("children") or []) if isinstance(c, dict) and bounds(c)]
    if not tb or not children:
        return tb

    child_bounds = [bounds(c) for c in children if bounds(c)]
    outside = sum(1 for cb in child_bounds if not intersects(tb, cb, tolerance=2))
    if outside <= len(child_bounds) * 0.5:
        return tb

    # Prefer a direct child with the same size as the target. This is usually
    # the local-space background/frame rectangle.
    for cb in child_bounds:
        if abs(cb["width"] - tb["width"]) <= 2 and abs(cb["height"] - tb["height"]) <= 2:
            return cb

    min_x = min(cb["x"] for cb in child_bounds)
    min_y = min(cb["y"] for cb in child_bounds)
    max_x = max(cb["x"] + cb["width"] for cb in child_bounds)
    max_y = max(cb["y"] + cb["height"] for cb in child_bounds)
    return {"x": min_x, "y": min_y, "width": max_x - min_x, "height": max_y - min_y}


def build_ir(root: Node, target_id: Optional[str]) -> Dict[str, Any]:
    target = find_by_id(root, target_id) if target_id else choose_target(root)
    if target is None:
        raise SystemExit(f"target node not found: {target_id}")

    raw_tb = bounds(target)
    tb = effective_target_bounds(target)
    if not tb:
        raise SystemExit("target node has no bounds")

    kept: List[Node] = []
    dropped = Counter()

    for node, ancestors in walk(target):
        t = node.get("type")
        if t not in VISIBLE_TYPES:
            dropped["unsupported_type"] += 1
            continue
        b = bounds(node)
        if not b:
            dropped["no_bounds"] += 1
            continue
        if not effective_visible(node, ancestors):
            dropped["hidden_or_opacity_zero"] += 1
            continue

        ancestor_outside = False
        for ancestor in ancestors:
            if ancestor is target:
                continue
            if ancestor.get("type") in CONTAINER_TYPES:
                ab = bounds(ancestor)
                if ab and not intersects(tb, ab, tolerance=2):
                    ancestor_outside = True
                    break
        if ancestor_outside:
            dropped["ancestor_outside_target"] += 1
            continue

        if not intersects(tb, b, tolerance=2):
            dropped["outside_target"] += 1
            continue
        # Keep target itself and in-bounds children; avoid unrelated huge descendants.
        if node is not target and not contains(tb, b, tolerance=4):
            dropped["not_contained"] += 1
            continue

        item: Node = {
            "id": node.get("id"),
            "name": node.get("name"),
            "type": t,
            "bounds": b,
            "role": classify_role(node, tb),
        }
        if node.get("characters") is not None:
            item["characters"] = node.get("characters")
        styles = normalize_styles(node.get("styles"))
        if styles:
            item["styles"] = styles
        if node.get("componentName"):
            item["componentName"] = node.get("componentName")
        if node.get("variantProperties"):
            item["variantProperties"] = node.get("variantProperties")
        if node.get("layout"):
            item["layout"] = node.get("layout")
        kept.append(item)

    kept_sorted = sorted(kept, key=lambda n: (bounds(n)["y"], bounds(n)["x"]))

    role_counts = Counter(n.get("role") for n in kept_sorted)
    type_counts = Counter(n.get("type") for n in kept_sorted)

    warnings = []
    if len(kept_sorted) > 250:
        warnings.append("IR still has many nodes; consider selecting a smaller target or fetching child nodes.")
    if role_counts.get("control-box", 0) and not role_counts.get("section-title", 0):
        warnings.append("Controls detected but no section titles; verify parser did not choose the wrong target.")

    return {
        "version": "1.1",
        "source": "figma-mcp-go-normalized",
        "target": {
            "id": target.get("id"),
            "name": target.get("name"),
            "type": target.get("type"),
            "rawBounds": raw_tb,
            "clipBounds": tb,
        },
        "summary": {
            "keptNodes": len(kept_sorted),
            "typeCounts": dict(type_counts),
            "roleCounts": dict(role_counts),
            "dropped": dict(dropped),
        },
        "tokens": collect_tokens(kept_sorted),
        "layout": infer_layout(kept_sorted, tb),
        "semanticNodes": kept_sorted,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Raw figma-mcp-go output JSON")
    parser.add_argument("--out", required=True, help="Output IR JSON path")
    parser.add_argument("--target-node-id", default=None, help="Exact selected Figma node ID")
    args = parser.parse_args()

    configure_stdio()

    payload = read_json(args.input)
    root = unwrap_mcp_payload(payload)
    ir = build_ir(root, args.target_node_id)
    write_json(args.out, ir)

    print(json.dumps({
        "target": ir["target"],
        "summary": ir["summary"],
        "warnings": ir["warnings"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

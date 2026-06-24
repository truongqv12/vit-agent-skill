#!/usr/bin/env python3
"""
Normalize a figma-mcp-go style JSON dump into a smaller implementation IR.

v1.2 changes:
- Treat rectangular VECTOR/RECTANGLE nodes as visual boxes, not just icons.
- Preserve shape CSS (`backgroundColor`, `borderColor`, `borderWidth`, etc.) in `css`.
- Add `renderHint` so agents know whether a VECTOR should become a CSS box, divider, icon, or SVG asset.
- Add `compositeControls` to pair background vectors with contained text/icon nodes.
- Read UTF-8/UTF-8-BOM safely on Windows.

Usage:
  python -X utf8 extract_figma_ir.py --input raw-output.json --out figma-ir.json --target-node-id 5675:288345
  python -X utf8 extract_figma_ir.py --input raw-output.json --out figma-ir.json
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

Node = Dict[str, Any]
Bounds = Dict[str, float]

CONTAINER_TYPES = {"FRAME", "GROUP", "COMPONENT", "COMPONENT_SET", "INSTANCE", "SECTION"}
SHAPE_TYPES = {"VECTOR", "RECTANGLE", "ELLIPSE", "LINE", "POLYGON", "STAR", "BOOLEAN_OPERATION"}
VISIBLE_TYPES = CONTAINER_TYPES | SHAPE_TYPES | {"TEXT"}

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
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def unwrap_mcp_payload(payload: Any) -> Node:
    """Accept raw node JSON or common MCP wrapper shapes."""
    if isinstance(payload, dict):
        context = payload.get("context")
        if isinstance(context, list) and context:
            first = context[0]
            if isinstance(first, dict):
                return first
        node = payload.get("node")
        if isinstance(node, dict):
            return node
        data = payload.get("data")
        if isinstance(data, dict):
            return unwrap_mcp_payload(data)
        return payload
    if isinstance(payload, list) and payload and isinstance(payload[0], dict):
        return payload[0]
    raise SystemExit("Unsupported Figma/MCP JSON payload shape")


def bounds(node: Node) -> Optional[Bounds]:
    b = node.get("bounds")
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


def center(b: Bounds) -> Tuple[float, float]:
    return (b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)


def point_in_bounds(point: Tuple[float, float], outer: Bounds, tolerance: float = 0.0) -> bool:
    x, y = point
    return (
        outer["x"] - tolerance <= x <= outer["x"] + outer["width"] + tolerance
        and outer["y"] - tolerance <= y <= outer["y"] + outer["height"] + tolerance
    )


def intersects(a: Bounds, b: Bounds, tolerance: float = 0.0) -> bool:
    return not (
        a["x"] + a["width"] < b["x"] - tolerance
        or b["x"] + b["width"] < a["x"] - tolerance
        or a["y"] + a["height"] < b["y"] - tolerance
        or b["y"] + b["height"] < a["y"] - tolerance
    )


def contains(outer: Bounds, inner: Bounds, tolerance: float = 0.0) -> bool:
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


def find_by_id(root: Node, target_id: Optional[str]) -> Optional[Node]:
    if not target_id:
        return None
    for node, _ in walk(root):
        if str(node.get("id")) == str(target_id):
            return node
    return None


def choose_target(root: Node) -> Node:
    """Heuristic fallback when target-node-id is omitted.

    Prefer a large frame/group whose name indicates a popup/modal/page.
    """
    candidates: List[Tuple[float, Node]] = []
    for node, _ in walk(root):
        t = node.get("type")
        b = bounds(node)
        if t in CONTAINER_TYPES and b and b["width"] >= 120 and b["height"] >= 80:
            name = str(node.get("name") or "").lower()
            score = area(node)
            if any(word in name for word in ["popup", "modal", "dialog", "screen", "page", "frame"]):
                score *= 1.25
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
    """Keep raw design style values from figma-mcp-go.

    For VECTOR/RECTANGLE nodes these styles are not decorative by default.
    They often represent actual backgrounds, borders, cards, controls, badges,
    overlays, and table rows.
    """
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
        "letterSpacing",
        "textAlignHorizontal",
        "textAlignVertical",
        "effects",
        "cornerRadius",
        "topLeftRadius",
        "topRightRadius",
        "bottomRightRadius",
        "bottomLeftRadius",
        "strokeWeight",
        "strokeAlign",
        "opacity",
        "blendMode",
    ]:
        if key in styles:
            out[key] = styles[key]
    return out


def _first_color(value: Any) -> Optional[str]:
    if isinstance(value, str) and value.startswith("#"):
        return value
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str) and item.startswith("#"):
                return item
            if isinstance(item, dict):
                # Future-proof if serializer starts exporting richer paint objects.
                color = item.get("color") or item.get("hex") or item.get("value")
                if isinstance(color, str) and color.startswith("#"):
                    return color
    return None


def _has_paint(value: Any) -> bool:
    return _first_color(value) is not None


def _px(value: Any) -> Optional[str]:
    if value is None or value == "mixed":
        return None
    try:
        n = float(value)
    except (TypeError, ValueError):
        return str(value)
    if math.isclose(n, round(n)):
        return f"{int(round(n))}px"
    return f"{round(n, 2)}px"


def css_from_node(node: Node, role: str) -> Dict[str, Any]:
    """Convert raw styles to implementation-friendly CSS hints.

    This does not replace visual diff. It simply prevents the coding agent from
    ignoring VECTOR fills/strokes that are actually UI backgrounds.
    """
    st = normalize_styles(node.get("styles"))
    node_type = node.get("type")
    b = bounds(node)
    css: Dict[str, Any] = {}

    fill = _first_color(st.get("fills"))
    stroke = _first_color(st.get("strokes"))

    if node_type == "TEXT":
        if fill:
            css["color"] = fill
        for src, dest in [
            ("fontFamily", "fontFamily"),
            ("fontSize", "fontSize"),
            ("fontWeight", "fontWeight"),
            ("lineHeight", "lineHeight"),
            ("letterSpacing", "letterSpacing"),
        ]:
            if src in st:
                css[dest] = _px(st[src]) if src in {"fontSize", "lineHeight", "letterSpacing"} else st[src]
        if st.get("textAlignHorizontal"):
            css["textAlign"] = str(st["textAlignHorizontal"]).lower()
        return {k: v for k, v in css.items() if v is not None}

    # Shape/vector styles. Large, rectangular VECTOR nodes are commonly
    # backgrounds/controls in flattened Figma exports.
    if fill:
        css["backgroundColor"] = fill
    if stroke:
        css["borderColor"] = stroke
        css["borderStyle"] = "solid"
        stroke_width = st.get("strokeWeight")
        css["borderWidth"] = _px(stroke_width) or "1px"

    radius_keys = ["cornerRadius", "topLeftRadius", "topRightRadius", "bottomRightRadius", "bottomLeftRadius"]
    if st.get("cornerRadius") is not None:
        css["borderRadius"] = _px(st.get("cornerRadius"))
    elif b and b["width"] == b["height"] and b["width"] <= 48 and role in {"icon", "avatar", "close-button"}:
        css["borderRadius"] = "9999px"

    if node.get("opacity") is not None:
        css["opacity"] = node.get("opacity")
    elif st.get("opacity") is not None:
        css["opacity"] = st.get("opacity")

    # Dividers commonly arrive as zero-height vectors with a stroke.
    if role == "divider" and stroke:
        css.pop("backgroundColor", None)
        css["borderTopColor"] = stroke
        css["borderTopStyle"] = "solid"
        css["borderTopWidth"] = css.get("borderWidth", "1px")
        css.pop("borderColor", None)
        css.pop("borderStyle", None)
        css.pop("borderWidth", None)

    return {k: v for k, v in css.items() if v is not None}


def render_hint(node: Node, role: str) -> str:
    node_type = node.get("type")
    b = bounds(node)
    st = normalize_styles(node.get("styles"))
    has_fill = _has_paint(st.get("fills"))
    has_stroke = _has_paint(st.get("strokes"))

    if node_type == "TEXT":
        return "text"
    if role == "divider":
        return "css-divider"
    if node_type in {"VECTOR", "RECTANGLE"}:
        if role in {"icon", "close-button", "chevron-icon", "calendar-icon", "upload-icon", "image-placeholder"}:
            return "svg-or-icon"
        if role in {"control-box", "button-bg", "modal-surface", "surface", "overlay", "card", "badge", "avatar"}:
            return "css-box"
        if b and (b["width"] >= 48 or b["height"] >= 32) and (has_fill or has_stroke):
            return "css-box"
        return "svg-or-icon"
    if node_type in {"ELLIPSE", "POLYGON", "STAR", "BOOLEAN_OPERATION", "LINE"}:
        return "svg-or-icon"
    if node_type in CONTAINER_TYPES:
        return "container"
    return "unknown"


def classify_role(node: Node, target_bounds: Optional[Bounds]) -> str:
    name = str(node.get("name") or "")
    node_type = node.get("type")
    text = str(node.get("characters") or "")
    b = bounds(node)
    st = normalize_styles(node.get("styles"))
    fill = _first_color(st.get("fills"))
    stroke = _first_color(st.get("strokes"))

    for role, pattern in ROLE_PATTERNS:
        if pattern.search(name) or pattern.search(text):
            return role

    if node_type == "TEXT":
        if TEXT_SECTION_RE.match(text.strip()) and len(text.strip()) <= 40:
            return "section-title"
        return "text"

    if not b:
        return "container" if node_type in CONTAINER_TYPES else "shape"

    if target_bounds and b["width"] >= target_bounds["width"] * 0.85 and b["height"] <= 2:
        return "divider"
    if target_bounds and b["height"] >= target_bounds["height"] * 0.85 and b["width"] <= 2:
        return "divider"

    if node_type in SHAPE_TYPES:
        if target_bounds:
            same_width = abs(b["width"] - target_bounds["width"]) <= 3
            same_height = abs(b["height"] - target_bounds["height"]) <= 3
            if same_width and same_height and fill:
                return "overlay" if fill.lower() in {"#0f172a", "#000000"} else "surface"

        if b["height"] >= 300 and b["width"] >= 300 and fill:
            return "modal-surface" if fill.lower() in {"#ffffff", "#fff"} else "surface"

        # Enterprise form fields/selects are frequently flattened as vector rectangles.
        if 28 <= b["height"] <= 52 and b["width"] >= 180 and node_type in {"VECTOR", "RECTANGLE"}:
            return "control-box"

        # Buttons are also often vector rectangles. Use width to avoid confusing
        # wide inputs with buttons.
        if 28 <= b["height"] <= 52 and 40 <= b["width"] <= 180 and (fill or stroke):
            return "button-bg"

        # Badges/chips.
        if 16 <= b["height"] <= 28 and 32 <= b["width"] <= 160 and fill:
            return "badge"

        # Avatar/circle-ish backgrounds.
        if abs(b["width"] - b["height"]) <= 2 and 24 <= b["width"] <= 48 and fill:
            return "avatar"

        if b["width"] <= 36 and b["height"] <= 36:
            return "icon"

        if (b["width"] >= 80 and b["height"] >= 24) and (fill or stroke):
            return "surface"

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
                    elif isinstance(item, dict):
                        c = _first_color([item])
                        if c:
                            colors[c] += 1
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
        "colors": colors.most_common(30),
        "fonts": fonts.most_common(10),
        "fontSizes": font_sizes.most_common(12),
        "fontWeights": font_weights.most_common(10),
        "radii": radii.most_common(12),
        "strokeWeights": strokes.most_common(10),
    }


def cluster_positions(values: List[float], tolerance: float = 6.0) -> List[float]:
    if not values:
        return []
    values = sorted(values)
    clusters: List[List[float]] = [[values[0]]]
    for value in values[1:]:
        avg = sum(clusters[-1]) / len(clusters[-1])
        if abs(value - avg) <= tolerance:
            clusters[-1].append(value)
        else:
            clusters.append([value])
    return [round(sum(c) / len(c), 2) for c in clusters]


def infer_layout(semantic_nodes: List[Node], target_bounds: Bounds) -> Dict[str, Any]:
    text_nodes = [n for n in semantic_nodes if n.get("type") == "TEXT" and bounds(n)]
    box_nodes = [
        n for n in semantic_nodes
        if n.get("role") in {"control-box", "button-bg", "surface", "modal-surface", "badge"} and bounds(n)
    ]

    xs = [bounds(n)["x"] for n in box_nodes if bounds(n)]
    widths = [bounds(n)["width"] for n in box_nodes if bounds(n)]
    ys = [bounds(n)["y"] for n in semantic_nodes if bounds(n)]

    sections = []
    for n in text_nodes:
        if n.get("role") == "section-title":
            b = bounds(n)
            sections.append({"text": n.get("characters"), "y": b["y"], "x": b["x"]})

    return {
        "target": target_bounds,
        "columns": cluster_positions(xs, tolerance=8),
        "commonBoxWidths": Counter(round(w) for w in widths).most_common(12),
        "rowYClusters": cluster_positions(ys, tolerance=4)[:100],
        "sections": sections,
    }


def effective_target_bounds(target: Node) -> Optional[Bounds]:
    """Return bounds used for clipping.

    Some serializers return the selected FRAME bounds in absolute canvas
    coordinates while children are normalized to local 0,0. When that happens,
    use a same-size background child or children extent as the clipping box.
    """
    tb = bounds(target)
    children = [c for c in (target.get("children") or []) if isinstance(c, dict) and bounds(c)]
    if not tb or not children:
        return tb

    child_bounds = [bounds(c) for c in children if bounds(c)]
    outside = sum(1 for cb in child_bounds if not intersects(tb, cb, tolerance=2))
    if outside <= len(child_bounds) * 0.5:
        return tb

    for cb in child_bounds:
        if abs(cb["width"] - tb["width"]) <= 2 and abs(cb["height"] - tb["height"]) <= 2:
            return cb

    min_x = min(cb["x"] for cb in child_bounds)
    min_y = min(cb["y"] for cb in child_bounds)
    max_x = max(cb["x"] + cb["width"] for cb in child_bounds)
    max_y = max(cb["y"] + cb["height"] for cb in child_bounds)
    return {"x": min_x, "y": min_y, "width": max_x - min_x, "height": max_y - min_y}


def build_composite_controls(nodes: List[Node]) -> List[Dict[str, Any]]:
    """Pair CSS-box vectors with text/icon layers contained within them.

    This gives the coding agent a semantic hint:
    - a VECTOR with role=button-bg plus text inside is a button
    - a VECTOR with role=control-box plus text/icon inside is an input/select
    - a VECTOR with role=badge plus text inside is a badge/chip
    """
    boxes = [
        n for n in nodes
        if n.get("renderHint") == "css-box"
        and n.get("role") in {"control-box", "button-bg", "badge", "avatar", "modal-surface", "surface"}
        and bounds(n)
    ]
    texts = [n for n in nodes if n.get("type") == "TEXT" and bounds(n)]
    icons = [n for n in nodes if n.get("renderHint") == "svg-or-icon" and bounds(n)]

    composites: List[Dict[str, Any]] = []
    used_child_ids = set()

    for box in boxes:
        bb = bounds(box)
        if not bb:
            continue
        contained_texts = [
            t for t in texts
            if point_in_bounds(center(bounds(t)), bb, tolerance=2)
            and t.get("id") not in used_child_ids
        ]
        contained_icons = [
            i for i in icons
            if point_in_bounds(center(bounds(i)), bb, tolerance=2)
            and i.get("id") not in used_child_ids
        ]

        element = None
        if box.get("role") == "button-bg" and contained_texts:
            element = "button"
        elif box.get("role") == "control-box":
            # A chevron/calendar contained in the box usually means select/date-picker.
            if any(i.get("role") in {"chevron-icon", "calendar-icon"} for i in contained_icons):
                element = "select-or-date-control"
            else:
                element = "input"
        elif box.get("role") == "badge" and contained_texts:
            element = "badge"
        elif box.get("role") in {"modal-surface", "surface"}:
            # Avoid creating huge composites for whole screens/cards unless useful.
            if len(contained_texts) <= 8 and len(contained_icons) <= 4:
                element = "surface"

        if not element:
            continue

        for child in contained_texts + contained_icons:
            used_child_ids.add(child.get("id"))

        composites.append({
            "element": element,
            "backgroundNodeId": box.get("id"),
            "bounds": bb,
            "role": box.get("role"),
            "css": box.get("css", {}),
            "text": " ".join(str(t.get("characters", "")).strip() for t in contained_texts).strip() or None,
            "textNodeIds": [t.get("id") for t in contained_texts],
            "iconNodeIds": [i.get("id") for i in contained_icons],
        })

    return composites


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
        if node is not target and not contains(tb, b, tolerance=4):
            dropped["not_contained"] += 1
            continue

        role = classify_role(node, tb)
        item: Node = {
            "id": node.get("id"),
            "name": node.get("name"),
            "type": t,
            "bounds": b,
            "role": role,
            "renderHint": render_hint(node, role),
        }

        if node.get("characters") is not None:
            item["characters"] = node.get("characters")

        styles = normalize_styles(node.get("styles"))
        if styles:
            item["styles"] = styles

        css = css_from_node(node, role)
        if css:
            item["css"] = css

        # Preserve MCP/plugin extras when available.
        for key in [
            "componentName",
            "variantProperties",
            "layout",
            "constraints",
            "opacity",
            "visible",
        ]:
            if node.get(key) is not None:
                item[key] = node.get(key)

        kept.append(item)

    kept_sorted = sorted(kept, key=lambda n: (bounds(n)["y"], bounds(n)["x"]))
    role_counts = Counter(n.get("role") for n in kept_sorted)
    type_counts = Counter(n.get("type") for n in kept_sorted)
    render_hint_counts = Counter(n.get("renderHint") for n in kept_sorted)

    css_boxes = [n for n in kept_sorted if n.get("renderHint") == "css-box"]
    composite_controls = build_composite_controls(kept_sorted)

    warnings = []
    if len(kept_sorted) > 250:
        warnings.append("IR still has many nodes; consider selecting a smaller target or fetching child nodes.")
    if role_counts.get("control-box", 0) and not role_counts.get("section-title", 0):
        warnings.append("Controls detected but no section titles; verify parser did not choose the wrong target.")
    if css_boxes and not any(n.get("css", {}).get("backgroundColor") or n.get("css", {}).get("borderColor") for n in css_boxes):
        warnings.append("CSS boxes detected but no fill/stroke CSS extracted; check MCP serializer styles.")
    if any(n.get("type") in SHAPE_TYPES and n.get("role") in {"control-box", "button-bg", "surface", "modal-surface"} and not n.get("css") for n in kept_sorted):
        warnings.append("Some shape/vector UI boxes have no css; serializer may be missing fills/strokes/cornerRadius.")

    return {
        "version": "1.2",
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
            "renderHintCounts": dict(render_hint_counts),
            "cssBoxCount": len(css_boxes),
            "compositeControls": len(composite_controls),
            "dropped": dict(dropped),
        },
        "tokens": collect_tokens(kept_sorted),
        "layout": infer_layout(kept_sorted, tb),
        "shapePrimitives": [
            {
                "id": n.get("id"),
                "name": n.get("name"),
                "type": n.get("type"),
                "role": n.get("role"),
                "renderHint": n.get("renderHint"),
                "bounds": n.get("bounds"),
                "css": n.get("css", {}),
            }
            for n in kept_sorted
            if n.get("renderHint") in {"css-box", "css-divider", "svg-or-icon"}
        ],
        "compositeControls": composite_controls,
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

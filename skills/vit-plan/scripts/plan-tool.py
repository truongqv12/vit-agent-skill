#!/usr/bin/env python3
"""Small, dependency-free filesystem helper for vit-plan/v1 artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "vit-plan/v1"
PLAN_FIELDS = {
    "schemaVersion",
    "title",
    "description",
    "status",
    "priority",
    "effort",
    "tags",
    "blockedBy",
    "blocks",
    "created",
}
PHASE_FIELDS = {"schemaVersion", "id", "title", "status", "dependencies"}
PLAN_REQUIRED = PLAN_FIELDS
PHASE_REQUIRED = PHASE_FIELDS
PLAN_STATUSES = {"pending", "in-progress", "blocked", "completed"}
PHASE_STATUSES = {"pending", "in-progress", "blocked", "completed"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
PLAN_SECTIONS = {
    "delivery contract",
    "phases",
    "dependencies",
    "success criteria",
    "risks and mitigations",
    "open questions",
}
PHASE_SECTIONS = {
    "context",
    "related files",
    "implementation steps",
    "todo",
    "validation",
    "risks and mitigations",
    "rollback",
}
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PLAN_DIR_RE = re.compile(r"(\d{6}-\d{4})-([a-z0-9]+(?:-[a-z0-9]+)*)\Z")
TIMESTAMP_RE = re.compile(r"\d{6}-\d{4}\Z")
PHASE_ID_RE = re.compile(r"phase-(\d{2})\Z")
PHASE_FILE_RE = re.compile(r"phase-(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md\Z")
SIMPLE_SCALAR_RE = re.compile(r"[A-Za-z0-9_./-]+\Z")
KEY_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*\Z")
WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
PHASE_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|\s*$"
)


class PlanToolError(Exception):
    """A safe, user-actionable helper failure."""


class Frontmatter(dict[str, Any]):
    """Parsed controlled values plus their source spelling for schema checks."""

    def __init__(self) -> None:
        super().__init__()
        self.sources: dict[str, str] = {}


def _safe_text(value: str, label: str) -> str:
    value = value.strip()
    if not value:
        raise PlanToolError(f"{label} must not be empty")
    if any(ord(char) < 32 for char in value):
        raise PlanToolError(f"{label} must be a single line without control characters")
    return value


def validate_slug(slug: str) -> str:
    if not SLUG_RE.fullmatch(slug):
        raise PlanToolError(
            "slug must be lowercase kebab-case using only ASCII letters and digits"
        )
    if len(slug) > 80:
        raise PlanToolError("slug must be 80 characters or fewer")
    if slug.upper() in WINDOWS_RESERVED:
        raise PlanToolError(f"slug '{slug}' is a Windows-reserved name")
    return slug


def slugify_title(title: str) -> str:
    title = re.sub(r"^\s*phase\s+\d+\s*:\s*", "", title, flags=re.IGNORECASE)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not slug:
        raise PlanToolError("phase title must contain an ASCII letter or digit for its filename")
    return validate_slug(slug[:80].rstrip("-"))


def _ensure_within(path: Path, root: Path, label: str) -> None:
    resolved_root = root.resolve(strict=False)
    resolved_path = path.resolve(strict=False)
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise PlanToolError(f"{label} escapes the explicit target root") from exc


def _reject_symlink_components(path: Path, label: str) -> None:
    current = path.absolute()
    while True:
        if current.is_symlink():
            raise PlanToolError(f"{label} contains a symbolic-link component: {current}")
        if current.parent == current:
            return
        current = current.parent


def _template_path(name: str) -> Path:
    return Path(__file__).resolve().parent.parent / "templates" / name


def _read_text(path: Path) -> tuple[str, bool, str]:
    raw = path.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise PlanToolError(f"{path}: file is not valid UTF-8") from exc
    newline = "\r\n" if b"\r\n" in raw else "\n"
    return text, has_bom, newline


def _encode_text(text: str, bom: bool = False) -> bytes:
    data = text.encode("utf-8")
    return (b"\xef\xbb\xbf" + data) if bom else data


def _render_template(path: Path, values: dict[str, str]) -> str:
    try:
        template, _, _ = _read_text(path)
    except FileNotFoundError as exc:
        raise PlanToolError(f"required template is missing: {path}") from exc
    for key, value in values.items():
        token = "{{" + key + "}}"
        quoted = json.dumps(value, ensure_ascii=False)
        template = template.replace(f'"{token}"', quoted)
        template = template.replace(f"'{token}'", quoted)
        template = template.replace(token, value)
    unresolved = sorted(set(re.findall(r"{{[A-Z][A-Z0-9_]*}}", template)))
    if unresolved:
        raise PlanToolError(
            f"template {path.name} contains unsupported placeholders: {', '.join(unresolved)}"
        )
    return template


def _write_new(path: Path, text: str) -> None:
    try:
        with path.open("xb") as handle:
            handle.write(_encode_text(text))
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise PlanToolError(f"refusing to overwrite existing path: {path}") from exc


def _atomic_write(path: Path, text: str, bom: bool, newline: str) -> None:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if newline != "\n":
        normalized = normalized.replace("\n", newline)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, delete=False
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(_encode_text(normalized, bom))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def _split_array_sources(source: str) -> list[str]:
    if not source.endswith("]"):
        raise ValueError("inline array is missing closing ']'")
    inner = source[1:-1].strip()
    if not inner:
        return []
    values: list[str] = []
    start = 0
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(inner):
        char = inner[index]
        if quote == '"':
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif quote == "'":
            if char == quote:
                if index + 1 < len(inner) and inner[index + 1] == "'":
                    index += 1
                else:
                    quote = None
        elif char in {'"', "'"}:
            quote = char
        elif char == ",":
            values.append(inner[start:index].strip())
            start = index + 1
        elif char in "[]{}":
            raise ValueError("nested collections are not supported")
        index += 1
    if quote is not None:
        raise ValueError("unterminated quoted value")
    values.append(inner[start:].strip())
    return values


def _parse_array(source: str) -> list[str]:
    return [_parse_scalar(item) for item in _split_array_sources(source)]


def _parse_scalar(source: str) -> str:
    if not source:
        raise ValueError("empty scalar")
    if source.startswith('"'):
        try:
            value = json.loads(source)
        except json.JSONDecodeError as exc:
            raise ValueError("invalid double-quoted scalar") from exc
        if not isinstance(value, str):
            raise ValueError("only string scalars are supported")
    elif source.startswith("'"):
        if len(source) < 2 or not source.endswith("'"):
            raise ValueError("invalid single-quoted scalar")
        value = source[1:-1].replace("''", "'")
    else:
        if not SIMPLE_SCALAR_RE.fullmatch(source):
            raise ValueError("unsupported unquoted scalar")
        value = source
    if any(ord(char) < 32 for char in value):
        raise ValueError("scalar must be one line without control characters")
    return value


def parse_frontmatter(path: Path, text: str) -> tuple[Frontmatter, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise PlanToolError(f"{path}: frontmatter must start with '---' on the first line")
    closing = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if closing is None:
        raise PlanToolError(f"{path}: frontmatter is missing its closing '---'")
    data = Frontmatter()
    for line_number, raw_line in enumerate(lines[1:closing], 2):
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise PlanToolError(f"{path}:{line_number}: expected 'field: value'")
        key, source = line.split(":", 1)
        key = key.strip()
        source = source.strip()
        if not KEY_RE.fullmatch(key):
            raise PlanToolError(f"{path}:{line_number}: unsupported field name '{key}'")
        if key in data:
            raise PlanToolError(f"{path}:{line_number}: duplicate field '{key}'")
        try:
            data[key] = _parse_array(source) if source.startswith("[") else _parse_scalar(source)
            data.sources[key] = source
        except ValueError as exc:
            raise PlanToolError(f"{path}:{line_number}: {key}: {exc}") from exc
    body = "".join(lines[closing + 1 :])
    return data, body


def _headings(body: str) -> set[str]:
    return {
        match.group(1).strip().lower()
        for match in re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    }


def _validate_fields(
    path: Path, data: dict[str, Any], required: set[str], allowed: set[str]
) -> list[str]:
    errors: list[str] = []
    for field in sorted(required - data.keys()):
        errors.append(f"{path}: missing required frontmatter field '{field}'")
    for field in sorted(data.keys() - allowed):
        errors.append(f"{path}: unknown frontmatter field '{field}'")
    return errors


def _validate_sections(path: Path, body: str, required: set[str]) -> list[str]:
    present = _headings(body)
    return [f"{path}: missing required section '## {name.title()}'" for name in sorted(required - present)]


def _validate_delivery_contract(path: Path, body: str) -> list[str]:
    match = re.search(
        r"^##\s+Delivery Contract\s*$\n(.*?)(?=^##\s|\Z)",
        body.replace("\r\n", "\n"),
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return []
    present = {
        heading.strip().lower()
        for heading in re.findall(r"^###\s+(.+?)\s*$", match.group(1), flags=re.MULTILINE)
    }
    required = {"outcome", "constraints", "non-goals", "acceptance criteria"}
    return [
        f"{path}: Delivery Contract is missing '### {name.title()}'"
        for name in sorted(required - present)
    ]


def _phase_rows(plan_path: Path, body: str) -> tuple[list[tuple[int, str, str, str]], list[str]]:
    rows: list[tuple[int, str, str, str]] = []
    errors: list[str] = []
    in_phases = False
    for line in body.splitlines():
        if re.fullmatch(r"##\s+Phases\s*", line, flags=re.IGNORECASE):
            in_phases = True
            continue
        if in_phases and line.startswith("## "):
            break
        if not in_phases or not line.lstrip().startswith("|"):
            continue
        match = PHASE_ROW_RE.fullmatch(line.strip())
        if match:
            rows.append((int(match.group(1)), match.group(2).strip(), match.group(3).strip(), match.group(4).strip()))
        elif "[" in line and "](" in line:
            errors.append(f"{plan_path}: malformed phase table row: {line.strip()}")
    return rows, errors


def _validate_related_paths(path: Path, body: str) -> list[str]:
    errors: list[str] = []
    match = re.search(
        r"^##\s+Related Files\s*$\n(.*?)(?=^##\s|\Z)",
        body.replace("\r\n", "\n"),
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return errors
    for stored_path in re.findall(r"^\s*-.*?`([^`]+)`", match.group(1), flags=re.MULTILINE):
        if (
            stored_path.startswith(("/", "\\", "~"))
            or re.match(r"^[A-Za-z]:[\\/]", stored_path)
            or "\\" in stored_path
            or ".." in Path(stored_path).parts
            or "://" in stored_path
        ):
            errors.append(f"{path}: related file path must be repo-relative with forward slashes: {stored_path}")
    return errors


def _is_repo_relative(value: str) -> bool:
    return not (
        not value
        or value.startswith(("/", "\\", "~"))
        or re.match(r"^[A-Za-z]:[\\/]", value)
        or "\\" in value
        or ".." in Path(value).parts
        or "://" in value
    )


def _is_quoted(source: str) -> bool:
    return len(source) >= 2 and source[0] in {'"', "'"} and source[-1] == source[0]


def _validate_plan_frontmatter(path: Path, data: Frontmatter) -> list[str]:
    errors = _validate_fields(path, data, PLAN_REQUIRED, PLAN_FIELDS)
    if data.get("schemaVersion") != SCHEMA_VERSION:
        errors.append(f"{path}: schemaVersion must be '{SCHEMA_VERSION}'")
    if data.get("status") not in PLAN_STATUSES:
        errors.append(f"{path}: invalid plan status '{data.get('status')}'")
    if data.get("priority") not in PRIORITIES:
        errors.append(f"{path}: priority must be one of {', '.join(sorted(PRIORITIES))}")
    for field in ("title", "description", "effort", "created"):
        if field in data and not isinstance(data[field], str):
            errors.append(f"{path}: field '{field}' must be a scalar string")
    for field in ("schemaVersion", "title", "description", "effort", "created"):
        if field in data.sources and not _is_quoted(data.sources[field]):
            errors.append(f"{path}: field '{field}' must be quoted")
    for field in ("title", "description"):
        if isinstance(data.get(field), str) and not data[field].strip():
            errors.append(f"{path}: field '{field}' must not be empty")
    for field in ("tags", "blockedBy", "blocks"):
        if field in data and not isinstance(data[field], list):
            errors.append(f"{path}: field '{field}' must be an inline array")
    created = data.get("created")
    if isinstance(created, str):
        try:
            dt.date.fromisoformat(created)
        except ValueError:
            errors.append(f"{path}: created must be an ISO date (YYYY-MM-DD)")
    for field in ("blockedBy", "blocks"):
        values = data.get(field)
        if isinstance(values, list):
            for value in values:
                if not _is_repo_relative(value):
                    errors.append(f"{path}: {field} path must be repo-relative: {value}")
    return errors


def _validate_phase_frontmatter(path: Path, data: Frontmatter) -> list[str]:
    errors = _validate_fields(path, data, PHASE_REQUIRED, PHASE_FIELDS)
    if data.get("schemaVersion") != SCHEMA_VERSION:
        errors.append(f"{path}: schemaVersion must be '{SCHEMA_VERSION}'")
    if data.get("status") not in PHASE_STATUSES:
        errors.append(f"{path}: invalid phase status '{data.get('status')}'")
    if not isinstance(data.get("id"), str) or not PHASE_ID_RE.fullmatch(data.get("id", "")):
        errors.append(f"{path}: id must match 'phase-NN'")
    if not isinstance(data.get("title"), str):
        errors.append(f"{path}: title must be a scalar string")
    elif not data["title"].strip():
        errors.append(f"{path}: title must not be empty")
    for field in ("schemaVersion", "id", "title"):
        if field in data.sources and not _is_quoted(data.sources[field]):
            errors.append(f"{path}: field '{field}' must be quoted")
    if not isinstance(data.get("dependencies"), list):
        errors.append(f"{path}: dependencies must be an inline array")
    elif any(not PHASE_ID_RE.fullmatch(value) for value in data["dependencies"]):
        errors.append(f"{path}: every dependency must match 'phase-NN'")
    elif data.get("dependencies"):
        try:
            sources = _split_array_sources(data.sources["dependencies"])
        except (KeyError, ValueError):
            sources = []
        if sources and any(not _is_quoted(source) for source in sources):
            errors.append(f"{path}: dependency IDs must be quoted")
    return errors


def lint_plan(plan_dir: Path | str) -> list[str]:
    plan_dir = Path(plan_dir)
    plan_path = plan_dir / "plan.md"
    if not plan_dir.is_dir():
        return [f"{plan_dir}: plan directory does not exist"]
    if not plan_path.is_file():
        return [f"{plan_path}: plan.md does not exist"]
    errors: list[str] = []
    directory_match = PLAN_DIR_RE.fullmatch(plan_dir.name)
    directory_date: dt.date | None = None
    if directory_match is None:
        errors.append(
            f"{plan_dir}: plan directory must match 'YYMMDD-HHMM-kebab-slug'"
        )
    else:
        try:
            directory_date = dt.datetime.strptime(directory_match.group(1), "%y%m%d-%H%M").date()
        except ValueError:
            errors.append(f"{plan_dir}: plan directory contains an invalid calendar timestamp")
    try:
        plan_text, _, _ = _read_text(plan_path)
        plan_data, plan_body = parse_frontmatter(plan_path, plan_text)
    except (OSError, PlanToolError) as exc:
        return [str(exc)]
    errors.extend(_validate_plan_frontmatter(plan_path, plan_data))
    if directory_date is not None and isinstance(plan_data.get("created"), str):
        try:
            created_date = dt.date.fromisoformat(plan_data["created"])
        except ValueError:
            pass
        else:
            if created_date != directory_date:
                errors.append(
                    f"{plan_path}: created date must match the plan directory calendar date"
                )
    errors.extend(_validate_sections(plan_path, plan_body, PLAN_SECTIONS))
    errors.extend(_validate_delivery_contract(plan_path, plan_body))
    slug_match = re.search(r"<!--\s*slug:\s*([^\s]+)\s*-->", plan_body)
    if directory_match and slug_match and slug_match.group(1) != directory_match.group(2):
        errors.append(f"{plan_path}: slug marker must match the plan directory slug")
    repo_root = plan_dir.parent.parent if plan_dir.parent.name == "plans" else plan_dir.parent
    for field in ("blockedBy", "blocks"):
        values = plan_data.get(field)
        if not isinstance(values, list):
            continue
        for value in values:
            if not _is_repo_relative(value):
                continue
            related_plan = repo_root / value
            try:
                _ensure_within(related_plan, repo_root, f"{field} path")
            except PlanToolError as exc:
                errors.append(f"{plan_path}: {exc}")
                continue
            if not (related_plan / "plan.md").is_file():
                errors.append(f"{plan_path}: {field} plan does not exist: {value}")
    rows, row_errors = _phase_rows(plan_path, plan_body)
    errors.extend(row_errors)

    phase_paths = sorted(path for path in plan_dir.glob("phase-*.md") if path.is_file())
    phase_data: dict[str, tuple[Path, dict[str, Any]]] = {}
    file_numbers: list[int] = []
    for path in phase_paths:
        file_match = PHASE_FILE_RE.fullmatch(path.name)
        if not file_match:
            errors.append(f"{path}: phase filename must match 'phase-NN-kebab-slug.md'")
            continue
        file_number = int(file_match.group(1))
        file_numbers.append(file_number)
        try:
            phase_text, _, _ = _read_text(path)
            data, body = parse_frontmatter(path, phase_text)
        except (OSError, PlanToolError) as exc:
            errors.append(str(exc))
            continue
        errors.extend(_validate_phase_frontmatter(path, data))
        errors.extend(_validate_sections(path, body, PHASE_SECTIONS))
        errors.extend(_validate_related_paths(path, body))
        phase_id = data.get("id")
        if isinstance(phase_id, str):
            if phase_id in phase_data:
                errors.append(f"{path}: duplicate phase id '{phase_id}'")
            else:
                phase_data[phase_id] = (path, data)
            id_match = PHASE_ID_RE.fullmatch(phase_id)
            if id_match and int(id_match.group(1)) != file_number:
                errors.append(f"{path}: filename number does not match id '{phase_id}'")

    expected_numbers = list(range(1, len(file_numbers) + 1))
    if sorted(file_numbers) != expected_numbers:
        errors.append(
            f"{plan_dir}: phase filenames must be unique and sequential from 01; found {sorted(file_numbers)}"
        )
    if not phase_paths:
        errors.append(f"{plan_dir}: at least one phase file is required")

    linked_names: list[str] = []
    row_numbers: list[int] = []
    for row_number, _title, target, _status in rows:
        row_numbers.append(row_number)
        if not target.startswith("./") or "/" in target[2:] or "\\" in target:
            errors.append(f"{plan_path}: phase link must be a local './phase-NN-slug.md' path: {target}")
            continue
        name = target[2:]
        link_match = PHASE_FILE_RE.fullmatch(name)
        if not link_match:
            errors.append(f"{plan_path}: invalid phase link target '{target}'")
        elif int(link_match.group(1)) != row_number:
            errors.append(f"{plan_path}: phase row {row_number} links a mismatched phase number: {target}")
        linked_names.append(name)
        if not (plan_dir / name).is_file():
            errors.append(f"{plan_path}: broken phase link '{target}'")
    if row_numbers != list(range(1, len(rows) + 1)):
        errors.append(f"{plan_path}: phase table rows must be sequential from 1")
    actual_names = [path.name for path in phase_paths]
    if len(linked_names) != len(set(linked_names)):
        errors.append(f"{plan_path}: phase table contains duplicate file links")
    missing_links = sorted(set(actual_names) - set(linked_names))
    extra_links = sorted(set(linked_names) - set(actual_names))
    if missing_links:
        errors.append(f"{plan_path}: phase files missing from table: {', '.join(missing_links)}")
    if extra_links:
        errors.append(f"{plan_path}: table links without phase files: {', '.join(extra_links)}")

    by_filename = {path.name: data for path, data in phase_data.values()}
    for _row_number, row_title, target, row_status in rows:
        name = target[2:] if target.startswith("./") else target
        data = by_filename.get(name)
        if data is None:
            continue
        if row_title != data.get("title"):
            errors.append(f"{plan_path}: table title for {target} does not match phase frontmatter")
        normalized_status = row_status.strip().lower().replace(" ", "-")
        if normalized_status not in PHASE_STATUSES:
            errors.append(f"{plan_path}: invalid phase table status '{row_status}'")
        elif normalized_status != data.get("status"):
            errors.append(f"{plan_path}: table status for {target} does not match phase frontmatter")

    graph: dict[str, list[str]] = {}
    all_ids = set(phase_data)
    for phase_id, (path, data) in phase_data.items():
        dependencies = data.get("dependencies")
        if not isinstance(dependencies, list):
            continue
        graph[phase_id] = dependencies
        if phase_id in dependencies:
            errors.append(f"{path}: phase cannot depend on itself ('{phase_id}')")
        for dependency in dependencies:
            if dependency not in all_ids:
                errors.append(f"{path}: dependency '{dependency}' does not exist")
        if len(dependencies) != len(set(dependencies)):
            errors.append(f"{path}: dependencies must not contain duplicates")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, trail: list[str]) -> None:
        if node in visiting:
            start = trail.index(node)
            cycle = trail[start:] + [node]
            message = f"{plan_dir}: dependency cycle: {' -> '.join(cycle)}"
            if message not in errors:
                errors.append(message)
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency, trail + [dependency])
        visiting.remove(node)
        visited.add(node)

    for phase_id in sorted(graph):
        visit(phase_id, [phase_id])
    return errors


def create_plan(
    root: Path | str,
    slug: str,
    title: str,
    description: str | None = None,
    date: str | None = None,
    first_phase_title: str | None = None,
    timestamp: str | None = None,
) -> list[Path]:
    root = Path(root)
    _reject_symlink_components(root, "root")
    slug = validate_slug(slug)
    title = _safe_text(title, "title")
    description = _safe_text(description or title, "description")
    first_phase_title = _safe_text(first_phase_title or "Foundation", "first phase title")
    timestamp = timestamp or dt.datetime.now().strftime("%y%m%d-%H%M")
    if not TIMESTAMP_RE.fullmatch(timestamp):
        raise PlanToolError("timestamp must use YYMMDD-HHMM")
    try:
        timestamp_date = dt.datetime.strptime(timestamp, "%y%m%d-%H%M").date()
    except ValueError as exc:
        raise PlanToolError("timestamp must use YYMMDD-HHMM") from exc
    date = date or timestamp_date.isoformat()
    try:
        parsed_date = dt.date.fromisoformat(date)
    except ValueError as exc:
        raise PlanToolError("date must use YYYY-MM-DD") from exc
    if parsed_date != timestamp_date:
        raise PlanToolError("date must match the calendar date encoded by timestamp")

    target = root / f"{timestamp}-{slug}"
    _ensure_within(target, root, "plan directory")
    if target.exists() or target.is_symlink():
        raise PlanToolError(f"refusing target collision: {target}")
    plan_path = target / "plan.md"
    phase_name = f"phase-01-{slug}.md"
    phase_path = target / phase_name
    plan_text = _render_template(
        _template_path("plan.md"),
        {
            "TITLE": title,
            "DESCRIPTION": description,
            "SLUG": slug,
            "DATE": date,
            "FIRST_PHASE_TITLE": first_phase_title,
            "FIRST_PHASE_FILE": phase_name,
        },
    )
    phase_text = _render_template(
        _template_path("phase.md"),
        {"PHASE_ID": "phase-01", "PHASE_TITLE": first_phase_title, "DEPENDENCIES": "[]"},
    )

    created_root_dirs: list[Path] = []
    target_created = False
    created: list[Path] = []
    try:
        if not root.exists():
            current = root
            while not current.exists():
                created_root_dirs.append(current)
                current = current.parent
            root.mkdir(parents=True)
        if not root.is_dir():
            raise PlanToolError(f"root is not a directory: {root}")
        _ensure_within(target, root, "plan directory")
        target.mkdir()
        target_created = True
        _write_new(plan_path, plan_text)
        created.append(plan_path)
        _write_new(phase_path, phase_text)
        created.append(phase_path)
        return created
    except Exception:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        if target_created:
            try:
                target.rmdir()
            except OSError:
                pass
        for directory in created_root_dirs:
            try:
                directory.rmdir()
            except OSError:
                break
        raise


def _normalize_dependencies(values: Iterable[str] | None) -> list[str]:
    dependencies: list[str] = []
    for value in values or []:
        dependencies.extend(item.strip() for item in value.split(",") if item.strip())
    if len(dependencies) != len(set(dependencies)):
        raise PlanToolError("dependencies must not contain duplicates")
    for dependency in dependencies:
        if not PHASE_ID_RE.fullmatch(dependency):
            raise PlanToolError(f"dependency must match 'phase-NN': {dependency}")
    return dependencies


def _append_phase_row(plan_path: Path, text: str, row: str) -> str:
    newline = "\r\n" if "\r\n" in text else "\n"
    normalized = text.replace("\r\n", "\n")
    lines = normalized.splitlines(keepends=True)
    heading = next(
        (i for i, line in enumerate(lines) if re.fullmatch(r"##\s+Phases\s*\n?", line, re.IGNORECASE)),
        None,
    )
    if heading is None:
        raise PlanToolError(f"{plan_path}: missing '## Phases' section")
    insert_at: int | None = None
    for index in range(heading + 1, len(lines)):
        line = lines[index]
        if line.startswith("## "):
            break
        if PHASE_ROW_RE.fullmatch(line.strip()):
            insert_at = index + 1
    if insert_at is None:
        raise PlanToolError(f"{plan_path}: phases table has no valid phase row")
    lines.insert(insert_at, row + "\n")
    return "".join(lines).replace("\n", newline) if newline == "\r\n" else "".join(lines)


def add_phase(
    plan_dir: Path | str, title: str, dependencies: Iterable[str] | None = None
) -> list[Path]:
    plan_dir = Path(plan_dir)
    _reject_symlink_components(plan_dir, "plan directory")
    title = _safe_text(title, "title")
    dependencies = _normalize_dependencies(dependencies)
    existing_errors = lint_plan(plan_dir)
    if existing_errors:
        raise PlanToolError("cannot add a phase until lint errors are fixed:\n  " + "\n  ".join(existing_errors))
    plan_path = plan_dir / "plan.md"
    plan_text, bom, newline = _read_text(plan_path)
    phase_paths = sorted(plan_dir.glob("phase-*.md"))
    next_number = len(phase_paths) + 1
    if next_number > 99:
        raise PlanToolError("vit-plan/v1 supports at most 99 phases")
    phase_id = f"phase-{next_number:02d}"
    existing_ids = {f"phase-{number:02d}" for number in range(1, next_number)}
    missing = sorted(set(dependencies) - existing_ids)
    if phase_id in dependencies:
        raise PlanToolError(f"phase cannot depend on itself ('{phase_id}')")
    if missing:
        raise PlanToolError(f"dependencies do not exist: {', '.join(missing)}")
    phase_slug = slugify_title(title)
    phase_name = f"{phase_id}-{phase_slug}.md"
    phase_path = plan_dir / phase_name
    _ensure_within(phase_path, plan_dir, "phase file")
    if phase_path.exists() or phase_path.is_symlink():
        raise PlanToolError(f"refusing phase collision: {phase_path}")
    dependency_literal = json.dumps(dependencies, ensure_ascii=False)
    phase_text = _render_template(
        _template_path("phase.md"),
        {"PHASE_ID": phase_id, "PHASE_TITLE": title, "DEPENDENCIES": dependency_literal},
    )
    row = f"| {next_number} | [{title}](./{phase_name}) | Pending |"
    updated_plan = _append_phase_row(plan_path, plan_text, row)
    created = False
    try:
        _write_new(phase_path, phase_text)
        created = True
        _atomic_write(plan_path, updated_plan, bom, newline)
    except Exception:
        if created:
            phase_path.unlink(missing_ok=True)
        raise
    return [phase_path, plan_path]


def _print_paths(paths: Iterable[Path]) -> None:
    for path in paths:
        print(path.resolve())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create and lint portable vit-plan/v1 Markdown artifacts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="create a plan and its first phase")
    create_parser.add_argument("--root", required=True, type=Path, help="explicit parent directory")
    create_parser.add_argument("--slug", required=True, help="lowercase kebab-case plan slug")
    create_parser.add_argument("--title", required=True, help="plan title")
    create_parser.add_argument("--description", help="plan description (defaults to title)")
    create_parser.add_argument("--date", help="creation date as YYYY-MM-DD (defaults to today)")
    create_parser.add_argument(
        "--timestamp", help="directory timestamp as YYMMDD-HHMM (defaults to current local time)"
    )
    create_parser.add_argument("--first-phase-title", help="first phase title (defaults to Foundation)")

    add_parser = subparsers.add_parser("add-phase", help="append one sequential phase")
    add_parser.add_argument("plan_dir", type=Path, help="explicit plan directory containing plan.md")
    add_parser.add_argument("--title", required=True, help="phase title")
    add_parser.add_argument(
        "--dependencies",
        nargs="*",
        default=[],
        metavar="PHASE_ID",
        help="existing phase IDs, separated by spaces or commas",
    )

    lint_parser = subparsers.add_parser("lint", help="validate a vit-plan/v1 plan directory")
    lint_parser.add_argument("plan_dir", type=Path, help="explicit plan directory containing plan.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "create":
            _print_paths(
                create_plan(
                    args.root,
                    args.slug,
                    args.title,
                    args.description,
                    args.date,
                    args.first_phase_title,
                    args.timestamp,
                )
            )
        elif args.command == "add-phase":
            _print_paths(add_phase(args.plan_dir, args.title, args.dependencies))
        else:
            errors = lint_plan(args.plan_dir)
            if errors:
                for error in errors:
                    print(f"error: {error}", file=sys.stderr)
                return 1
            print(f"valid: {Path(args.plan_dir).resolve()}")
        return 0
    except (PlanToolError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

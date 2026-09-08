#!/usr/bin/env python3
"""Standalone regression tests for plan-tool.py."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("plan-tool.py")
TEMPLATES = SCRIPT.parent.parent / "templates"
SPEC = importlib.util.spec_from_file_location("vit_plan_tool", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import {SCRIPT}")
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)


class PlanToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        deadline = time.monotonic() + 10
        required = [TEMPLATES / "plan.md", TEMPLATES / "phase.md"]
        while time.monotonic() < deadline and not all(path.is_file() for path in required):
            time.sleep(0.1)
        missing = [str(path) for path in required if not path.is_file()]
        if missing:
            raise RuntimeError("canonical templates are required: " + ", ".join(missing))

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "plans"

    def create(self, slug: str = "sample-plan") -> Path:
        TOOL.create_plan(
            self.root,
            slug,
            'Kế hoạch "portable"',
            "Mô tả UTF-8",
            "2026-08-24",
            "Discovery",
            "260824-1516",
        )
        return self.root / f"260824-1516-{slug}"

    @staticmethod
    def replace(path: Path, old: str, new: str) -> None:
        text = path.read_text(encoding="utf-8-sig")
        if old not in text:
            raise AssertionError(f"test fixture does not contain {old!r}: {path}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")

    def assert_lint_error(self, plan_dir: Path, fragment: str) -> None:
        errors = TOOL.lint_plan(plan_dir)
        self.assertTrue(errors, "lint unexpectedly succeeded")
        self.assertIn(fragment.lower(), "\n".join(errors).lower())

    def test_create_and_lint_round_trip_utf8_and_quoted_scalar(self) -> None:
        plan_dir = self.create()
        self.assertEqual([], TOOL.lint_plan(plan_dir))
        self.assertIn('Kế hoạch "portable"', (plan_dir / "plan.md").read_text(encoding="utf-8"))
        self.assertTrue((plan_dir / "phase-01-sample-plan.md").is_file())

    def test_add_phase_with_dependency_updates_plan_and_round_trips(self) -> None:
        plan_dir = self.create()
        paths = TOOL.add_phase(plan_dir, "Implementation", ["phase-01"])
        phase = plan_dir / "phase-02-implementation.md"
        self.assertEqual(phase, paths[0])
        self.assertTrue(phase.is_file())
        self.assertIn('dependencies: ["phase-01"]', phase.read_text(encoding="utf-8"))
        self.assertIn("./phase-02-implementation.md", (plan_dir / "plan.md").read_text(encoding="utf-8"))
        self.assertEqual([], TOOL.lint_plan(plan_dir))

    def test_collision_refuses_overwrite(self) -> None:
        plan_dir = self.create()
        before = {path.name: path.read_bytes() for path in plan_dir.iterdir()}
        with self.assertRaisesRegex(TOOL.PlanToolError, "collision"):
            TOOL.create_plan(
                self.root,
                "sample-plan",
                "Different",
                date="2026-08-24",
                timestamp="260824-1516",
            )
        after = {path.name: path.read_bytes() for path in plan_dir.iterdir()}
        self.assertEqual(before, after)

    def test_invalid_and_reserved_slugs_cannot_escape_root(self) -> None:
        for slug in ("../escape", "nested/escape", "CON", "con", "bad_slug", "bad."):
            with self.subTest(slug=slug), self.assertRaises(TOOL.PlanToolError):
                TOOL.create_plan(
                    self.root,
                    slug,
                    "Unsafe",
                    date="2026-08-24",
                    timestamp="260824-1516",
                )
        self.assertFalse((self.base / "escape").exists())
        self.assertFalse(self.root.exists())

    def test_symbolic_link_root_is_refused(self) -> None:
        outside = self.base / "outside"
        outside.mkdir()
        linked_root = self.base / "linked-plans"
        try:
            os.symlink(outside, linked_root, target_is_directory=True)
        except (OSError, NotImplementedError):
            original = Path.is_symlink

            def simulated_symlink(path: Path) -> bool:
                return path.absolute() == linked_root.absolute() or original(path)

            with mock.patch.object(Path, "is_symlink", simulated_symlink):
                with self.assertRaisesRegex(TOOL.PlanToolError, "symbolic-link"):
                    TOOL.create_plan(
                        linked_root,
                        "escape-plan",
                        "Escape",
                        date="2026-08-24",
                        timestamp="260824-1516",
                    )
        else:
            with self.assertRaisesRegex(TOOL.PlanToolError, "symbolic-link"):
                TOOL.create_plan(
                    linked_root,
                    "escape-plan",
                    "Escape",
                    date="2026-08-24",
                    timestamp="260824-1516",
                )
        self.assertFalse((outside / "260824-1516-escape-plan").exists())

    def test_canonical_directory_name_and_timestamp_are_enforced(self) -> None:
        plan_dir = self.create()
        self.replace(plan_dir / "plan.md", "<!-- slug: sample-plan -->", "<!-- slug: other-plan -->")
        self.assert_lint_error(plan_dir, "slug marker")
        self.replace(plan_dir / "plan.md", "<!-- slug: other-plan -->", "<!-- slug: sample-plan -->")
        renamed = self.root / "sample-plan"
        plan_dir.rename(renamed)
        self.assert_lint_error(renamed, "YYMMDD-HHMM-kebab-slug")
        for index, bad_timestamp in enumerate(
            ("20260824-1516", "26824-1516", "260824-516", "260232-1516", "260824-2460")
        ):
            with self.subTest(timestamp=bad_timestamp), self.assertRaisesRegex(
                TOOL.PlanToolError, "timestamp"
            ):
                TOOL.create_plan(
                    self.root,
                    f"bad-time-{index}",
                    "Bad time",
                    date="2026-08-24",
                    timestamp=bad_timestamp,
                )
        with self.assertRaisesRegex(TOOL.PlanToolError, "date must match"):
            TOOL.create_plan(
                self.root,
                "bad-date",
                "Bad date",
                date="2026-08-23",
                timestamp="260824-1516",
            )

        date_dir = self.create("directory-date")
        mismatched_dir = self.root / "260823-1516-directory-date"
        date_dir.rename(mismatched_dir)
        self.assert_lint_error(mismatched_dir, "created date must match")

    def test_invalid_status_schema_unknown_field_and_malformed_frontmatter(self) -> None:
        cases = (
            ('status: pending', 'status: impossible', "invalid plan status"),
            ('schemaVersion: "vit-plan/v1"', 'schemaVersion: "vit-plan/v2"', "schemaVersion"),
            ('status: pending', 'mystery: value\nstatus: pending', "unknown frontmatter field"),
            ('title: "Kế hoạch \\"portable\\""', 'title: {unsupported: mapping}', "unsupported unquoted scalar"),
        )
        for index, (old, new, expected) in enumerate(cases):
            with self.subTest(expected=expected):
                plan_dir = self.create(f"case-{index}")
                self.replace(plan_dir / "plan.md", old, new)
                self.assert_lint_error(plan_dir, expected)

        multiline_dir = self.create("multiline-value")
        self.replace(
            multiline_dir / "plan.md",
            'description: "Mô tả UTF-8"',
            'description: "line one\\nline two"',
        )
        self.assert_lint_error(multiline_dir, "one line")

    def test_broken_link_is_reported(self) -> None:
        plan_dir = self.create()
        self.replace(
            plan_dir / "plan.md",
            "./phase-01-sample-plan.md",
            "./phase-01-missing.md",
        )
        self.assert_lint_error(plan_dir, "broken phase link")

    def test_missing_duplicate_and_gapped_phase_ids_are_reported(self) -> None:
        missing_dir = self.create("missing-id")
        phase = missing_dir / "phase-01-missing-id.md"
        self.replace(phase, 'id: "phase-01"\n', "")
        self.assert_lint_error(missing_dir, "missing required frontmatter field 'id'")

        duplicate_dir = self.create("duplicate-id")
        TOOL.add_phase(duplicate_dir, "Second", ["phase-01"])
        self.replace(duplicate_dir / "phase-02-second.md", 'id: "phase-02"', 'id: "phase-01"')
        self.assert_lint_error(duplicate_dir, "duplicate phase id")

        gap_dir = self.create("gapped-id")
        TOOL.add_phase(gap_dir, "Second", ["phase-01"])
        old_phase = gap_dir / "phase-02-second.md"
        new_phase = gap_dir / "phase-03-second.md"
        old_phase.rename(new_phase)
        self.replace(new_phase, 'id: "phase-02"', 'id: "phase-03"')
        self.replace(gap_dir / "plan.md", "| 2 |", "| 3 |")
        self.replace(gap_dir / "plan.md", "phase-02-second.md", "phase-03-second.md")
        self.assert_lint_error(gap_dir, "sequential from 01")

    def test_self_missing_and_cyclic_dependencies_are_reported(self) -> None:
        self_dir = self.create("self-dependency")
        self.replace(self_dir / "phase-01-self-dependency.md", "dependencies: []", 'dependencies: ["phase-01"]')
        self.assert_lint_error(self_dir, "cannot depend on itself")

        missing_dir = self.create("missing-dependency")
        self.replace(missing_dir / "phase-01-missing-dependency.md", "dependencies: []", 'dependencies: ["phase-99"]')
        self.assert_lint_error(missing_dir, "does not exist")

        cycle_dir = self.create("cycle-dependency")
        TOOL.add_phase(cycle_dir, "Second", ["phase-01"])
        self.replace(cycle_dir / "phase-01-cycle-dependency.md", "dependencies: []", 'dependencies: ["phase-02"]')
        self.assert_lint_error(cycle_dir, "dependency cycle")

    def test_utf8_bom_and_crlf_are_tolerated_and_preserved_on_update(self) -> None:
        plan_dir = self.create()
        for path in plan_dir.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            path.write_bytes(b"\xef\xbb\xbf" + text.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual([], TOOL.lint_plan(plan_dir))
        TOOL.add_phase(plan_dir, "Résumé", ["phase-01"])
        plan_bytes = (plan_dir / "plan.md").read_bytes()
        self.assertTrue(plan_bytes.startswith(b"\xef\xbb\xbf"))
        self.assertIn(b"\r\n", plan_bytes)
        self.assertEqual([], TOOL.lint_plan(plan_dir))

    def test_related_file_path_must_be_repo_relative(self) -> None:
        plan_dir = self.create()
        phase = plan_dir / "phase-01-sample-plan.md"
        self.replace(phase, "`path/to/new-file`", "`C:\\outside\\file.py`")
        self.assert_lint_error(plan_dir, "repo-relative")

    def test_create_rolls_back_partial_files_and_new_directories(self) -> None:
        root = self.base / "new-parent" / "plans"
        real_write_new = TOOL._write_new
        calls = 0

        def fail_second_write(path: Path, text: str) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected create failure")
            real_write_new(path, text)

        with mock.patch.object(TOOL, "_write_new", side_effect=fail_second_write):
            with self.assertRaisesRegex(OSError, "injected create failure"):
                TOOL.create_plan(
                    root,
                    "rollback-plan",
                    "Rollback",
                    date="2026-08-24",
                    timestamp="260824-1516",
                )
        self.assertEqual(2, calls)
        self.assertFalse((root / "260824-1516-rollback-plan").exists())
        self.assertFalse(root.exists())
        self.assertTrue(self.base.exists())

    def test_add_phase_rolls_back_new_phase_when_plan_replace_fails(self) -> None:
        plan_dir = self.create()
        plan_path = plan_dir / "plan.md"
        original = plan_path.read_bytes()
        with mock.patch.object(TOOL, "_atomic_write", side_effect=OSError("injected replace failure")):
            with self.assertRaisesRegex(OSError, "injected replace failure"):
                TOOL.add_phase(plan_dir, "Second", ["phase-01"])
        self.assertEqual(original, plan_path.read_bytes())
        self.assertFalse((plan_dir / "phase-02-second.md").exists())

    def test_cli_help_and_validation_exit_codes(self) -> None:
        help_run = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, help_run.returncode, help_run.stderr)
        self.assertIn("{create,add-phase,lint}", help_run.stdout)
        missing_run = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), "lint", str(self.base / "missing")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(1, missing_run.returncode)
        usage_run = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), "create"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(2, usage_run.returncode)


if __name__ == "__main__":
    unittest.main(verbosity=2)

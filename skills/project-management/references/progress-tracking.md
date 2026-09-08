# Progress Tracking

## Plan Analysis Workflow

1. **Read plans directory:** Search for `plans/*/plan.md` to discover all plans.
2. **Parse YAML frontmatter:** Extract status, priority, effort, tags, created.
3. **Scan phase files:** Count `[x]` (done) vs `[ ]` (remaining) in each phase
   `## Todo` section.
4. **Reconcile completed work:** Ensure all completed runtime items map to phase
   files (backfill stale earlier phases first).
5. **Calculate progress:** `completed / total * 100` per plan.
6. **Cross-reference:** Compare plan tasks against actual implementation.

## Status Update Protocol

Plan and phase files ARE the store — there is no external plan database. Update
them directly.

### Native status updates (default)

1. Update each phase's `## Todo` checkboxes to reflect real completion.
2. Derive the phase's frontmatter `status` from its checkbox state
   (none checked → `pending`, some → `in-progress`, all → `completed`).
3. Update the matching Phases-table Status cell in `plan.md` — change only the
   cell text, preserve the table structure exactly.
4. Derive the plan's frontmatter `status` from the phase statuses.

### Optional verification

When a plan-linter helper is exposed, run it after edits to confirm the plan and
phase files stay internally consistent. In this repo:

```
python skills/vit-plan/scripts/plan-tool.py lint <plan-dir>
```

It checks that each Phases-table Status cell matches its phase frontmatter and
that the `vit-plan/v1` schema holds. Absent that helper, re-read the edited files
and confirm the table and frontmatter agree by eye.

### Plan-Level Status

Derive `plan.md` frontmatter `status`:

| Condition | Status |
|-----------|--------|
| No phases started | `pending` |
| Any phase in progress | `in-progress` |
| A phase blocked with no progress path | `blocked` |
| All phases complete | `completed` |

### Phase-Level Status

Each `phase-XX-*.md` tracks work with `## Todo` checkboxes:
- `[ ]` = pending item
- `[x]` = completed item
- Count the ratio for the phase progress percentage, then set the phase
  frontmatter `status` accordingly.

### Runtime Work Status

When a live task-management surface exists, mirror pending, active, blocked, and
completed work there. Otherwise, update the active plan directly. Plan checkboxes
remain authoritative across sessions.

### Reconciliation Rule

If a later phase is marked done while earlier phases still contain stale
unchecked completed items, backfill earlier phases in the same sync pass before
final status reporting.

## Verification Checklist

When verifying task completeness:

1. **Acceptance criteria met?** — Check against plan requirements.
2. **Code quality validated?** — A review capability's report available, or an
   inline review performed?
3. **Tests passing?** — A test capability confirms the suite is green, or focused
   checks were run inline?
4. **Documentation updated?** — Docs match implementation where impact exists?
5. **No regressions?** — Existing functionality intact?

## Report Generation

### Status Summary Template

```markdown
## Project Status: [Date]

### Active Plans
| Plan | Progress | Priority | Status |
|------|----------|----------|--------|
| [name] | [X]% | P[N] | [status] |

### Completed This Session
- [x] [description]

### Blockers & Risks
- [ ] [description] — [mitigation]

### Next Steps
1. [Priority action]
2. [Follow-up]
```

### Detailed Report Template

```markdown
## [Plan Name] - Detailed Status

### Achievements
- Completed features, resolved issues, delivered value

### Testing Status
- Components needing validation, test scenarios, quality gates

### Risk Assessment
- Potential blockers, technical debt, mitigation strategies

### Recommendations
- Prioritized next steps, resource needs, timeline projections
```

## Metrics to Track

- **Phase completion %** — How much of each phase is done.
- **Blocker count** — Open blockers preventing progress.
- **Dependency chain health** — Any circular or stale dependencies.
- **Time since last update** — Identify stale plans needing attention.
- **Test coverage** — Per-feature test pass rates.

# Output Standards

Follow the schema and naming authority in [plan-organization.md](plan-organization.md)
and use the physical templates under `../templates/`. Do not restate or invent a
second frontmatter schema in a plan.

## Plan quality

- Keep the delivery contract explicit: outcome, constraints, non-goals, and
  observable acceptance criteria.
- Make each phase implementable from its own context while keeping shared
  decisions in `plan.md`.
- List concrete repo-relative files and actions. Use `None identified` when the
  file cannot yet be known, then record the evidence gap.
- Order steps by dependency. State APIs, data shapes, migration rules, and
  failure handling precisely enough for implementation.
- Give every phase a focused validation gate, specific risks and mitigations,
  and a safe rollback path.
- Keep open questions last. Write `None` when no material question remains.
- Prefer concise bullets and tables over repeated prose. Do not copy mutable
  implementation inventories into multiple files.

## Evidence rules

- Current-code claims require direct repository evidence. Cite `path:line` for
  symbols, call paths, endpoints, configuration, and consumers.
- Greenfield design claims cannot cite code that does not exist. Cite the exact
  plan or phase heading that owns the proposed contract and label assumptions.
- External claims use authoritative current documentation when available. Link
  the source and distinguish quoted fact from inference.
- Mark unresolved claims `[UNVERIFIED]`; never turn intent into asserted current
  behavior.
- Research reports are supporting evidence, not durable plan authority. Carry
  the relevant decision and citation into the owning plan section.

## Task breakdown

- Each todo item names an action and observable deliverable.
- Dependencies are explicit and cycle-free.
- Parallel work has exclusive file ownership and a stated integration point.
- Checked items require completion evidence; do not use checkboxes as optimism.
- `--tdd` phases identify tests before the change, the protected change, tests
  for new behavior, and the regression gate.

## Completion and handoff

Before calling a plan ready:

1. Structurally lint it with the helper or native checklist.
2. Complete the mode's verification, validation, and red-team gates.
3. Re-read the full plan after any review edit.
4. Confirm no unresolved contradiction or blocking question remains.
5. Report the plan path, selected mode, completed gates, and any evidence gaps.

The planning workflow stops there. Implementation starts only through a
separate capability chosen by the user.


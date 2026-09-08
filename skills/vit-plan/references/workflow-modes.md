# Workflow Modes

Choose the smallest mode that produces enough evidence for the task. An
explicit mode wins. Without one, infer from scope and uncertainty; ask only
when two modes would materially change cost or review depth.

## Detection

| Signal | Mode |
|---|---|
| Small, clear, familiar, few dependencies | `fast` |
| Complex, unfamiliar, or externally constrained | `hard` |
| Major refactor across five or more areas | `deep` |
| Three or more independently ownable work streams | `parallel` |
| Two materially viable designs remain | `two` |

The [scope challenge](scope-challenge.md) may recommend a smaller or larger
mode, but an explicit user scope decision remains authoritative.

## Fast

Use for clear, low-risk work.

1. Reuse the accepted delivery contract.
2. Inspect repository instructions and the directly affected source/tests.
3. Skip external research and the formal scope challenge.
4. Write the smallest complete plan and apply the Fact Checker role.
5. Run validation or red-team only when requested or when inspection reveals a
   material risk.

Fast means proportional planning, not evidence-free planning.

## Hard

Use for complex work or unfamiliar constraints.

1. Investigate two independent concerns or approaches.
2. Inspect the owning code paths, tests, contracts, and current documentation.
3. Synthesize one recommended design with explicit trade-offs.
4. Apply Standard or Full verification based on phase count.
5. Run red-team review, then decision validation.

Independent investigation may be delegated concurrently. Without delegation,
perform the same investigations sequentially and keep their evidence separate
until synthesis.

## Deep

Use for large refactors or broad architectural debt. Follow Hard mode and add
for every phase:

- file inventory with action and ownership;
- test scenario matrix for critical and failure paths;
- function, interface, endpoint, or configuration checklist;
- dependency map and integration gate;
- rollback boundary.

Run Full verification, red-team review, decision validation, and the mandatory
whole-plan consistency sweep.

## Parallel

Use only when ownership can be disjoint.

- Define exclusive file ownership for each concurrent phase.
- Show parallel groups and sequential integration phases in `plan.md`.
- State conflict prevention and merge/integration checks.
- Keep dependency direction acyclic.
- Apply the Hard review gates.

If delegation is unavailable, execute the research and review work
sequentially. Preserve the parallel implementation graph in the plan; do not
invent overlapping ownership merely to simulate concurrency.

## Two approaches

1. Research two genuinely viable approaches against the same delivery
   contract.
2. Compare complexity, risk, compatibility, rollback, and effort.
3. Recommend one, but ask the user to select before producing implementation
   phases.
4. Plan only the selected approach, then apply the Hard review gates.

Do not keep both approaches as competing executable phases.

## Composable options

### `--tdd`

For each implementation phase, specify:

1. regression tests that capture current behavior;
2. seams or infrastructure needed for safe change;
3. the protected implementation change;
4. tests for new behavior;
5. the compile, type, and test regression gate.

### `--no-tasks`

Skip runtime work-item projection. Markdown statuses and checkboxes remain the
complete tracking surface.


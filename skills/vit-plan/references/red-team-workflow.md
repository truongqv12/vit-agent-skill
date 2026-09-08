# Red-Team Workflow

Adversarially review a complete implementation plan for failure modes,
unsupported assumptions, threat gaps, and accidental complexity. Reviewers
find problems; the controller adjudicates evidence; the user decides which
material corrections to apply.

## Resolve and read

Resolve the plan from an explicit path, a live active-plan capability, or a
unique project-local unfinished-plan match. Ask when resolution is ambiguous.
Read `plan.md` and every phase file in full before reviewing.

## Scale the review

Load [red-team-personas.md](red-team-personas.md).

| Phase count | Lenses |
|---|---|
| 1-2 | Security Adversary, Assumption Destroyer |
| 3-5 | Add Failure Mode Analyst |
| 6+ | Add Scope and Complexity Critic |

Optional delegates may run independent lenses concurrently. If unavailable,
run each lens sequentially. Do not reduce the selected lenses or evidence
standard merely because concurrency is absent.

## Finding contract

Each finding must contain:

- severity: Critical, High, or Medium;
- precise plan location;
- concrete flaw and failure scenario;
- evidence;
- smallest cause-aligned correction.

Evidence rules:

- Claims about existing code require `repo/relative/path:line` evidence and a
  traced or inspected code path.
- Greenfield contract omissions and internal plan contradictions cite exact
  document and heading, such as `phase-02-foo.md > Validation`.
- External facts cite authoritative current documentation.
- Reject evidence-free findings. Do not reject a valid plan-structure finding
  merely because no implementation exists yet.

Collect, deduplicate, sort by severity, and cap the final set at fifteen.
Exclude naming, formatting, lint, and generic best-practice observations that
do not threaten the delivery contract.

## Adjudicate

For each surviving finding, propose `Accept` or `Reject` with a specific
rationale. A verified existing decision stays in place unless the finding adds
new evidence or the context changed.

Present the adjudicated set to the user. Offer to apply all accepted findings,
review them individually, or reject them. For individual review, allow Accept,
Reject, or Accept with a user-provided modification.

Do not edit plan files before user adjudication. Do not silently reverse scope,
schema, architecture, risk tolerance, or another explicit user choice.

## Apply and reconcile

Apply only approved findings to their owning sections. Append a `## Red Team
Review` session to `plan.md` with date, counts, severity, disposition, evidence,
and affected phase. Keep rejected findings in the session record so they are
not repeatedly raised without new evidence.

Then run the [whole-plan consistency sweep](verification-roles.md#whole-plan-consistency-sweep).
If contradictions remain, list them as unresolved and stop before
implementation handoff.

## Report

- findings by severity and disposition;
- files changed;
- risks addressed;
- whole-plan sweep result;
- unresolved questions last.

Red-team review never implements the plan or performs external effects.


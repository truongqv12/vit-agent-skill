# Validation Workflow

Validate implementation decisions through evidence and a focused user
interview. This differs from structural `lint`: lint checks artifact shape;
validation checks whether the plan is correct, complete, and accepted.

## Resolve and read the plan

1. Prefer the explicit plan path.
2. Otherwise use a live active-plan capability only when it is actually
   exposed.
3. Otherwise scan project-local unfinished plans and ask the user when multiple
   candidates overlap.
4. Read `plan.md` and every `phase-*.md` file in full.

Stop with a clear path request if no unique plan can be resolved.

## Verify before asking

Load [verification-roles.md](verification-roles.md) and select the tier by
phase count. Verify paths, symbols, behavior, state lifetime, and consumers
against current repository evidence.

- Record `VERIFIED`, `FAILED`, and `UNVERIFIED` claims.
- Never auto-correct a failed or unverified claim.
- Turn material failures into interview topics with evidence-supported
  alternatives.
- If a prior red-team session already verified a claim and the evidence has not
  changed, reuse that verified decision instead of reversing it for an abstract
  concern.

## Build the interview

Load [validation-question-framework.md](validation-question-framework.md).
Prioritize questions that could change architecture, scope, compatibility,
security, data handling, rollout, rollback, or acceptance criteria.

Use a structured question capability when available. Otherwise ask the same
questions in plain conversation, one bounded group at a time. Simple plans may
need no questions when every material decision is already evidenced and
accepted.

## Adjudication rule

The user decides changes to intent, public contracts, risk tolerance, and other
material trade-offs. Before editing any plan file:

1. show the original claim or decision;
2. show the verification evidence or concern;
3. explain the trade-off;
4. present concrete options and a recommendation;
5. wait for the user's choice.

Do not silently reverse an explicit user decision. An audit may change it only
when it adds new evidence or the context changed, followed by renewed approval.

## Record and propagate

Append a `## Validation Log` session to `plan.md` with:

- trigger and date;
- verification tier and result counts;
- exact material questions and all presented options;
- the user's answer, including verbatim custom input;
- confirmed decisions and affected phases;
- action items and unresolved evidence.

Apply only approved changes. Update every affected plan summary, phase step,
dependency, risk, validation gate, and acceptance criterion. Avoid disposable
update-marker comments; the resulting plan should read as the current coherent
contract.

## Consistency gate

Run the [whole-plan consistency sweep](verification-roles.md#whole-plan-consistency-sweep)
after propagation. Do not report the plan ready while any contradiction,
failed material claim, or blocking question remains.

## Report

Return:

- claims checked and verification results;
- questions asked and decisions confirmed;
- files and phases updated;
- whole-plan sweep result;
- recommendation to proceed or revise;
- unresolved questions last.

Validation never implements the plan or performs external effects.


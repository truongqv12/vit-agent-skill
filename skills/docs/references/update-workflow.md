# Update Workflow

Use this workflow to reconcile project documentation with current intent and
evidence. An update is not a mandate to touch every document; scope every edit
to the authority surface whose contract or evidence actually changed. Read
`references/doc-content-rules.md` before authoring or delegating changes.

## 1. Brainstorm the impact

Run the opening gate from the parent skill. Define the changed contract, the
affected audience, the accepted scope, and the proof required.

## 2. Discover authority and evidence

- Read repository instructions, the root README, and the existing docs route.
- Enumerate current docs with repository search tools; do not assume a flat
  directory or a standard file count.
- Inspect the changed source, tests, scripts, generated artifacts, and relevant
  live state.
- Map each changed claim to its current owner. Detect duplicate prose, obsolete
  paths, and stateful records presented as evergreen truth.
- Flag prose that re-describes code, hand-maintains counts or inventories, or
  would be falsified by an implementation rename.

Use parallel readers only when the corpus is large enough to benefit, the
runtime exposes a delegation capability, and the user's request permits it;
otherwise read inline with native tools. Partition by independent topics, not
arbitrary file-count thresholds.

## 3. Reconcile minimally

Use a documentation-authoring capability through delegation when the runtime
exposes it and the user's request permits it; otherwise perform the same work
inline with native tools (read, search, shell). If neither path is possible,
stop and report the missing capability honestly. Include the relevant
ownership, drift-resistance, and per-document rules from
`references/doc-content-rules.md` in any delegated context.

Prune, do not refresh: delete implementation-describing prose or convert it to
a pointer. Preserve WHY content such as decisions, rationale, domain rules, and
terminology.

- Edit only impacted authority surfaces.
- Remove stale and duplicate material.
- Point repeated commands and inventories to their owning script, manifest, or
  generated source.
- Preserve unrelated valid docs.
- Do not add version notes, issue references, ADRs, or governance machinery just
  to record that an update occurred.

## 4. Validate

- Run the repository's existing docs validator when one exists.
- Verify internal links, referenced paths, examples, config keys, and commands.
- Run owning generators or contract scripts when generated or executable docs
  changed.
- Review the final route from a cold-start human and AI perspective.
- Report changed claims, their evidence, validation, and unresolved questions.

**Do not implement product code during this workflow.**

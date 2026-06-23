# Spec Generation Workflow

Use `templates/feature-spec.md` as the canonical Markdown structure. Generate it inside the output package directory defined by `references/output-packaging-rules.md`; never as a loose root file.

## Required sections

1. Metadata tài liệu, including output package, Epic, and Story.
2. Tóm tắt đầu vào.
3. Nhật ký bằng chứng.
4. Legend nguồn & độ tin cậy.
5. Tổng quan tính năng.
6. Mục tiêu nghiệp vụ.
7. Phạm vi.
8. Vai trò / tác nhân.
9. User stories.
10. Luồng nghiệp vụ.
11. Functional requirements.
12. Business rules.
13. Data requirements.
14. Validation rules.
15. Permission matrix.
16. State transition.
17. Edge cases & error handling.
18. Acceptance criteria.
19. NFR ở mức BA.
20. Audit / analytics / logging.
21. Dependencies.
22. Assumptions.
23. Open questions.
24. Traceability matrix.
25. Dev / QA handoff notes.
26. Quality checklist.

## Optional sections

Use these when relevant:

- Existing behavior.
- Requested change.
- Change impact.
- Backward compatibility.
- Regression risks.
- Figma notes.
- API notes.
- Glossary.

## Minimum viable spec

If input is small but user asks to proceed, produce a minimum viable spec with:

- Overview.
- Roles.
- Scope.
- Main flow.
- Functional requirements.
- Business rules.
- State transitions.
- Acceptance criteria.
- Assumptions.
- Open questions.

## Practicality rule

Prefer useful BA handoff over academic length. Include enough detail for dev/QA to implement and test, but do not pad the document.


## Figma link requirement

If Figma URLs exist, `feature-spec.md` must include:

- `2.4 Nhật ký bằng chứng Figma` with original clickable URLs.
- `2.5 Danh mục link Figma gốc` with every original user-provided Figma URL.

A node ID alone is not enough for dev/QA handoff.

## Output location requirement

Keep the output package path short. Use `ba-spec-output/YYYYMMDD/feature-slug/` by default and store Epic/Story details in metadata, not in the folder path.

`feature-spec.md` and `feature-spec.html` must be created inside the package folder, for example:

```text
ba-spec-output/20260623/cong-chung-dien-tu-truc-tiep/feature-spec.md
```

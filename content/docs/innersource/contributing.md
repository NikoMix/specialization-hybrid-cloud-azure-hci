---
title: "Innersource – Contributing"
description: "How consultants who run Azure Local engagements contribute improvements back to this repo."
linkTitle: "Contributing"
weight: 1
---

This is the consultant-facing view of `CONTRIBUTING.md`. Read both before
opening your first PR.

## What counts as a valuable contribution

- A new common gap surfaced in an audit
- A clarification or correction to an evidence checklist
- A new variant of a deliverable template
- A reference-architecture pattern not yet documented
- A lesson learned (good or bad) from a real engagement

## What does **not** belong here

- Customer-identifying information of any kind
- Credentials, secrets, tenant IDs, subscription IDs
- Vendor-specific pricing or contractual content
- Personal opinions unsupported by spec PDF or engagement evidence

## Workflow

1. Open an issue using one of the three templates (`control-improvement`,
   `template-improvement`, `lesson-learned`).
2. Wait for triage (2 business days SLA).
3. Branch from `main` as `feat/`, `fix/`, or `docs/`.
4. Make the change; run `hugo --gc` and the verification scripts locally.
5. Open a PR using the repo's PR template; tag CODEOWNERS.
6. Address review feedback; merge once approvals are in.

## Quality bar

| Aspect | Bar |
|---|---|
| Specificity | Name the exact control, page, line, or template. |
| Evidence | Cite spec PDF page, Microsoft Learn link, or engagement. |
| Anonymisation | Customers referred to as Customer A, B, C. |
| Build | `hugo --gc` builds clean and `scripts/check-tables.py` passes. |
| Markdown | Follows `.github/memories/hugo-content.md` rules — tables at column 0. |

## Where to ask for help

Open a discussion or ping CODEOWNERS in the PR. Avoid private DMs — the
innersource model only works if the conversation stays in the repo.

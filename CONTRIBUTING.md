# Contributing

This repository is an **innersource partner-enablement toolkit** for the
*Hybrid Cloud Infrastructure with Microsoft Azure Local (Azure Stack HCI)*
Advanced Specialization. Every consultant who runs an engagement is expected
to contribute back: new evidence patterns, refreshed reference architectures,
template improvements, lessons learned.

## Ground rules

- Open an Issue **before** large changes (use the templates in
  `.github/ISSUE_TEMPLATE/`).
- Branch names: `feat/<short-slug>`, `fix/<short-slug>`, `docs/<short-slug>`.
- Keep PRs scoped — one control, one template, or one engagement-playbook
  page per PR where practical.
- Sign commits with the standard `Co-authored-by: Copilot` trailer when the
  change was drafted with assistance.

## Content rules (MDX)

Read `.github/memories/mdx-content.md` before editing pages. Key rules:

- Escape `<` in prose as `&lt;`.
- Filenames must **not** contain dots — Starlight strips them from slugs.
- Use only the three status icons: `⬜ 🟡 ✅`.
- Cross-link controls with **relative** paths and trailing slash.
- Tables must have a blank line before and after; escape `|` in cell text as
  `\|`; restructure tables wider than 5 columns into nested tables or lists.

## Review SLA

- Triage within **2 business days**.
- First-pass review within **5 business days**.
- Two approvals required for changes to audit control wording; one approval
  for engagement-playbook / innersource page edits.

## Lifecycle (every page)

Every content page is in one of four states, tracked in the page footer:

`Draft → Reviewed → Endorsed → Deprecated`

See `innersource/content-governance/` for who can endorse and how often each
content area is reviewed.

## Code of conduct

Be specific, prescriptive, and respectful. Disagreements about audit
interpretation should be resolved by reference to the official Microsoft
spec PDF — not by seniority.

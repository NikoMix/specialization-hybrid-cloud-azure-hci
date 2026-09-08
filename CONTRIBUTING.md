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

## Content rules (Markdown)

Read `.github/memories/hugo-content.md` before editing pages. Key rules:

- **Every table row starts at column 0.** Indentation turns a table into a code
  block — the exact defect that broke the previous Astro build. Never put a
  table inside a list item; use a `### Heading` instead.
- Shortcode `href` values must **not** start with `/` (`docs/module-b/`, not
  `/docs/module-b/`) — Hugo's `relURL` drops the Pages project sub-path
  otherwise. Ordinary Markdown links are unaffected; use `/docs/...` there.
- Never nest `{{< button >}}` inside `{{% alert %}}`.
- Filenames must **not** contain dots.
- Use only the three status icons: `⬜ 🟡 ✅`.
- Write `<` and `&` literally — the MDX escapes (`&lt;`, `&amp;`) are gone.
- Tables must have a blank line before and after; escape `|` in cell text as
  `\|`.

Before opening a PR:

```bash
hugo --gc
python scripts/check-tables.py
python scripts/check-links.py
bash .github/scripts/test-create-issues.sh
```

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

# Hugo content authoring rules

**Scope:** `content/**/*.md`

This site is built with [Hugo](https://gohugo.io/) and the
[ms-hugo-theme](https://github.com/NikoMix/ms-hugo-theme) Microsoft Fluent
theme. Control pages follow a **strict template** so the Engagement Agent and
the auto-generated GitHub Issues stay synchronised.

## ⚠️ Tables are the most important thing on this site

Nearly every control page is an evidence checklist expressed as a Markdown
table. The previous Astro/Starlight build silently broke them: MDX parses a
table indented four or more spaces — which is what happened inside a
`<TabItem>` — as an indented code block, so the checklist shipped as grey
preformatted text.

**Rules:**

| Rule | Why |
|---|---|
| Every table row starts at **column 0** | Four spaces of indentation turns the table into a code block |
| Never nest a table inside a Markdown list item | Use a `### Heading` instead of a numbered list item |
| A table inside `{{% tab %}}` or `{{% alert %}}` still starts at column 0 | Those shortcodes render their inner text as Markdown |
| Blank line before and after every table | Goldmark needs the block boundary |
| Escape a literal `\|` inside a cell | Otherwise it splits the cell |

`scripts/check-tables.py` enforces the first rule statically and then compares
the number of source tables with the number of `<table>` elements in `public/`.
It runs in CI on every push and pull request.

## ⚠️ Shortcode hrefs must not start with `/`

The theme's `card` and `button` shortcodes pass their `href` through Hugo's
`relURL`. Verified on Hugo 0.165 with baseURL `https://example.com/sub/`:

```text
relURL "/docs/module-b/"  ->  /docs/module-b/        ← sub-path DROPPED
relURL "docs/module-b/"   ->  /sub/docs/module-b/    ← correct
```

Because this site publishes to a GitHub Pages **project** URL
(`https://<owner>.github.io/<repo>/`), a leading slash produces a link that
works in local preview and 404s once published.

- ✅ `{{% card title="Module B" href="docs/module-b/" %}}`
- ❌ `{{% card title="Module B" href="/docs/module-b/" %}}`

Ordinary Markdown links are **not** affected — they go through the theme's link
render hook, which resolves them via `.Page.GetPage` to a full `RelPermalink`.
Write those as site-absolute logical paths with a leading slash:
`[Module B](/docs/module-b/)`.

`scripts/check-links.py` enforces this against the built output.

## ⚠️ Never nest `{{< button >}}` inside `{{% alert %}}`

`{{% %}}` shortcodes render their inner text as Markdown. The `button`
shortcode emits multi-line HTML whose closing `>` sits at column 0, which
Markdown reads as a blockquote — the anchor comes out HTML-escaped. Put the
button at the top level of the page instead.

## Front matter

```yaml
---
title: "B.1.1 – Azure Local Implementation Capability"   # full control title
description: "One sentence, used for SEO, search index and the page lede."
linkTitle: "1.1 Azure Local Implementation"              # short label in the nav
weight: 1                                                # order within its section
---
```

Top-level guide pages use tens (`overview` 10, `requirements` 20,
`audit-process` 30, `module-a` 40, `module-b` 50, `engagement` 60,
`innersource` 70, `evidence-tracker` 80, `faq` 90) so a new page can be slotted
between two without renumbering.

## Control page template (Module A / Module B)

Every file in `content/docs/module-a/` and `content/docs/module-b/` follows
this structure:

```markdown
---
title: "<MODULE>.<SECTION>.<ITEM> – <Short Title>"
description: "<One-sentence summary>"
linkTitle: "<SECTION>.<ITEM> <Short Title>"
weight: <integer>
---

## What the Auditor Checks

<Short prose paragraph>

**Typical questions:**
- <Q1>

---

## Required Evidence Checklist

| # | Evidence Item | Accepted Formats | Status |
|---|---|---|---|
| 1 | **<Item name>** | PDF, Word, Excel | ⬜ |

{{% alert type="tip" %}}
<Optional shortcut or pro tip>
{{% /alert %}}

---

## Evidence Guidance

### <Item 1 name>

---

## Evidence Status

| Item | Owner | Status | Last Updated | Notes |
|---|---|---|---|---|

---

## Common Gaps

| Gap | Remediation |
|---|---|
```

## Shortcodes available

| Starlight component (old) | Hugo shortcode (now) |
|---|---|
| `<Aside type="tip">` | `{{% alert type="tip" %}} … {{% /alert %}}` or `> [!TIP]` |
| `<CardGrid>` / `<Card>` | `{{< cards >}}` / `{{% card title="" href="" icon="" %}}` |
| `<Tabs>` / `<TabItem label="">` | `{{< tabs >}}` / `{{% tab title="" %}}` |
| `<Steps>` | A plain ordered list, or `### Phase N — …` headings |
| — | `{{< button href="" icon="" >}}Label{{< /button >}}` |
| — | `{{< badge "Preview" >}}`, `{{% accordion title="" %}}` |

`alert` types: `note`, `tip`, `important`, `warning`, `caution`.
Icon names come from the theme's `assets/svg/icons/` — `checkmark`, `document`,
`book`, `star`, `info`, `search`, `grid`, `flash`, `github`, `settings`,
`list`, `share`, `collections`, `thumb-like`, `warning`, `shield`.

## Status icons (mandatory)

| Icon | Meaning |
|---|---|
| `⬜` | Not started |
| `🟡` | In progress |
| `✅` | Complete |

## Cross-references

- Control numbers in prose always use dots: `A.2.1`, `B.3.1`.
- Cross-link controls with **Markdown links** using site-absolute logical
  paths: `[2.1 Service delivery methodology](/docs/module-a/2-1-service-delivery-methodology/)`.
  Hugo resolves these through `GetPage`, so a broken one is reported as
  `MS Fluent: broken link` during the build.
- **Filenames must not contain dots.** Use `2-1-foo.md`, not `2.1-foo.md`.
- Never link to GitHub Issues by hard-coded number — they vary per fork.

## When evidence requirements change

If you add, remove, or reword an evidence item in a control page, you **must**
make the matching edit to `.github/scripts/create-issues.sh` so the
auto-created issue checkboxes stay aligned. The doc and the issue are a single
source of truth in two forms. `bash .github/scripts/test-create-issues.sh`
asserts the script still produces 7 Module A and 6 Module B issues.

## Escaping

Hugo/Goldmark does **not** need the MDX escapes this content used to carry.
Write `<` and `&` literally; do not write `&lt;` or `&amp;`.

# Hybrid Cloud Infrastructure with Microsoft Azure Local — Advanced Specialization

> Engagement toolkit for Microsoft partners pursuing the **Hybrid Cloud Infrastructure with Microsoft Azure Local Advanced Specialization** audit.

---

## 🎯 Purpose

This repository gives consultants a structured, step-by-step engagement framework to guide partner organisations through the Advanced Specialization audit. It includes:

- **GitHub Issues** as the primary engagement task board — one issue per control with evidence checklists
- **Documentation site** (Hugo + the [ms-hugo-theme](https://github.com/NikoMix/ms-hugo-theme) Microsoft Fluent theme) with detailed evidence guidance for each control
- **Engagement Agent** — an AI assistant that guides consultants through the process
- **Automated issue creation** — recreates audit issues each year, 9 months before the next audit

> ⚠️ **Verify against the official spec PDF.** This repo was scaffolded from public Microsoft sources. Cross-check every Module B control, ACR threshold, and certification list against the current Microsoft-issued *Hybrid Cloud Infrastructure with Microsoft Azure Local Advanced Specialization* requirements document before relying on it in a live engagement. Pages flagged `TODO: verify against spec PDF` are particularly important.

---

## 🚀 Getting Started

This repo is a **GitHub Template**. Click **"Use this template"** (not Fork) to create your own copy.

### 1. Use this template

Click **Use this template → Create a new repository** and choose your GitHub organisation.

### 2. Set your site URL

Nothing to configure. The deploy workflow calls `actions/configure-pages` and
passes the resolved URL to Hugo with `--baseURL`, so a fresh copy publishes to
its own Pages URL with no edit.

Two optional repository variables (**Settings → Secrets and variables → Actions
→ Variables**):

| Variable | Purpose |
|---|---|
| `SITE_URL` | Base URL used in generated issue bodies. Defaults to the GitHub Pages project URL derived from the repository name. |

### 3. Enable GitHub Pages

Go to your repo → **Settings → Pages → Source** → select **GitHub Actions**.

### 4. Create the engagement issues

Go to **Actions → Create Audit Engagement Issues → Run workflow**.

Enter the year of the next audit (e.g. `2027`). This creates labelled issues and a milestone.

### 5. Done

- Issues appear as your engagement task board 📋
- The documentation site deploys automatically on push to `main` 🌐
- Use the Engagement Agent for guided assistance 🤖

---

## 🤖 Engagement Agent

This repo ships with a **GitHub Custom Agent** — a purpose-built Copilot agent that knows every audit control, evidence requirement, and common blocker for this specialization.

### Using the Engagement Agent on GitHub.com

1. Go to **github.com/copilot** (or open Copilot in your repo)
2. Click the agent selector dropdown
3. Choose **Engagement Agent**
4. Ask anything:

> *"What should we work on first?"*
> *"What evidence do we need for B.1.1?"*
> *"We don't have an AZ-801 holder — what are our options?"*
> *"How do we evidence an Azure Local cluster deployment without exposing customer names?"*

The agent reads the repository documentation and open GitHub Issues to give you contextual, step-by-step guidance.

### Using the Engagement Agent in VS Code

The agent is also available in **VS Code Copilot Chat** once the repo is open — select it from the agent dropdown in the Copilot Chat panel.

### Assigning the agent to an issue

You can assign the Engagement Agent to a GitHub Issue directly — it will read the control checklist, search the docs, and prescribe the next action.

The agent profile is defined in [`.github/agents/engagement-agent.agent.md`](.github/agents/engagement-agent.agent.md).

---

## 📅 Annual Audit Cycle

The `Create Audit Engagement Issues` workflow runs automatically on a **schedule** (default: March 1st each year) to create a fresh set of issues for the next audit cycle, 9 months after the previous audit — giving your team 3 months to re-collect evidence.

To adjust the schedule to match your audit timing:
- Open `.github/workflows/create-issues.yml`
- Change the cron month: `0 9 1 **3** *` → your audit month + 9

---

## 🖥️ Local Development

The site is built with **Hugo (extended)** — no Node toolchain, no `npm install`.
The theme lives in [its own repository](https://github.com/NikoMix/ms-hugo-theme)
and is never vendored here; the deploy workflow clones it at build time.

```bash
# 1. Install Hugo extended 0.146.0 or newer — https://gohugo.io/installation/
hugo version   # must print "+extended"

# 2. Fetch the theme the same way CI does
git clone --depth 1 https://github.com/NikoMix/ms-hugo-theme.git themes/ms-hugo-theme

# 3. Preview
hugo server
```

### Verification scripts

The build is guarded by three checks, all run by the deploy workflow on every
push and pull request:

```bash
hugo --gc
python scripts/check-tables.py            # every Markdown table reaches the HTML
python scripts/check-links.py             # every internal link resolves
bash .github/scripts/test-create-issues.sh  # issue automation still covers Module B
```

`check-tables.py` exists because the previous Astro/Starlight build silently
rendered any table indented four or more spaces — for example inside a
`<TabItem>` — as a grey code block instead of a table. Evidence checklists are
tables, so that failure mode is a content defect, not a cosmetic one.

`check-links.py` exists because the theme's `card` and `button` shortcodes pass
their `href` through Hugo's `relURL`, which **drops the project sub-path when
the value starts with `/`**. Always write shortcode hrefs without a leading
slash (`docs/module-b/`, not `/docs/module-b/`). Markdown links are unaffected —
they go through the theme's link render hook and resolve correctly either way.

---

## 📁 Structure

```
├── .github/
│   ├── agents/engagement-agent.agent.md   # GitHub Custom Agent definition
│   ├── memories/hugo-content.md           # Content authoring rules
│   ├── scripts/create-issues.sh           # Issue creation script
│   ├── scripts/test-create-issues.sh      # Offline test for the above
│   └── workflows/
│       ├── deploy.yml                     # Hugo build, checks, deploy to Pages
│       └── create-issues.yml              # Annual issue creation
├── config/_default/                       # Hugo site configuration
│   ├── hugo.toml  markup.toml  params.toml  menus.en.toml
├── content/
│   ├── _index.md                          # Home page
│   └── docs/                              # The guide (left-hand navigation)
│       ├── overview.md  requirements.md  audit-process.md
│       ├── module-a/                      # Controls A.1.1 – A.3.3 (generic)
│       ├── module-b/                      # Controls B.1.1 – B.4.2 (Azure Local)
│       ├── engagement/                    # Delivery playbook + deliverables
│       └── innersource/                   # How to contribute
├── scripts/                               # check-tables.py, check-links.py,
│                                          # generate_workfiles.py
└── static/templates/                      # Downloadable Word/Excel/PowerPoint
```

---

## 📄 License

Content is provided for partner enablement purposes. Refer to your Microsoft Partner Agreement for usage terms.

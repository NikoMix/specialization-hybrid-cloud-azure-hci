---
title: "Engagement – Reference Architectures"
description: "Curated reference architectures for Azure Local engagements, linking to the official Azure Architecture Center where possible."
linkTitle: "6 · Reference architectures"
weight: 6
---

## When to use this

During discovery (to pick a starting pattern) and design (to anchor the HLD
to a recognised topology). Always link to the **official** Azure
Architecture Center article rather than redrawing — it lowers maintenance.

## Patterns we cover

{{< cards >}}
{{% card title="Single-site 4-node cluster" icon="settings" %}}
Standard datacentre pattern. 4 validated nodes, dual ToR, switchless
storage optional. Suits 50–200 VMs.
{{% /card %}}
{{% card title="Branch 2-node switchless" icon="collections" %}}
Edge / branch pattern. 2 nodes, switchless storage, cloud witness.
Suits 5–30 VMs per site, dozens of sites.
{{% /card %}}
{{% card title="Single-node Azure Local (far edge)" icon="document" %}}
Ruggedised single node for far-edge sites with no second node and
limited connectivity.
{{% /card %}}
{{% card title="Stretched cluster (multi-site)" icon="share" %}}
Two sites, site-aware fault domains, synchronous or asynchronous
replication, automated failover.
{{% /card %}}
{{% card title="AKS on Azure Local" icon="settings" %}}
Container platform on top of Azure Local — for line-of-business apps
that need orchestration on-prem.
{{% /card %}}
{{% card title="Arc-enabled SQL MI on Azure Local" icon="collections" %}}
Managed SQL with Azure-style operations, running on Azure Local nodes
via Arc-enabled data services.
{{% /card %}}
{{< /cards >}}

## Pattern selection grid

The customer's discovery answers map to a pattern as follows:

| Customer signal | Recommended starting pattern |
|---|---|
| One datacentre, refresh of 3-tier infra | Single-site 4-node cluster |
| Many branches, low VM count per site | Branch 2-node switchless |
| Far-edge, intermittent connectivity | Single-node Azure Local |
| Two paired datacentres, DR requirement | Stretched cluster |
| Container-first modern apps on-prem | AKS on Azure Local |
| Sovereign SQL workload on-prem | Arc-enabled SQL MI on Azure Local |

## Decision inputs

| # | Input | Why it matters |
|---|---|---|
| 1 | Site count + per-site host count | Drives switchless vs. switched, cluster size |
| 2 | RPO / RTO per workload tier | Drives stretch vs. backup-only DR |
| 3 | Workload profile (VM / container / SQL) | Drives AKS / Arc-SQL add-ons |
| 4 | Connectivity per site | Drives witness choice + Arc proxy config |
| 5 | Regulatory drivers | Drives secured-core + WDAC + sovereignty patterns |

## Output: customer-ready deliverable

A one-page pattern-selection memo cross-referenced to the HLD. Each
selected pattern in the HLD must cite the matching Azure Architecture
Center article URL — keep this list as a living index in the workbook.

{{% alert type="caution" %}}
This repo intentionally does **not** redraw diagrams. The Azure
Architecture Center diagrams change frequently; copying them creates
drift. Link to the live URL and embed only customer-specific overlays.
{{% /alert %}}

## Reuse & contribute back

{{% alert type="tip" %}}
If you delivered a variant the table doesn't cover (e.g. GPU at edge, AVD
on Azure Local), open a PR adding a new card + a row to the selection
grid.
{{% /alert %}}

---
title: "Engagement – Reference Architectures"
description: "Verified mapping from each Azure Local delivery pattern to its official Azure Architecture Center article, plus the documented gaps where no Architecture Center article exists."
linkTitle: "6 · Reference architectures"
weight: 6
---

## When to use this

During discovery (to pick a starting pattern) and design (to anchor the HLD to
a recognised topology). Always cite the **official** Microsoft article rather
than redrawing it — it lowers maintenance and, more importantly, gives the
auditor a published Microsoft reference against which your delivered
architecture can be checked for control
[B.1.1](/docs/module-b/1-1-azure-local-implementation/).

{{% alert type="important" title="Every URL below was fetched and verified" %}}
Each link was retrieved and its title confirmed. Where a Microsoft page
redirects to a version-monikered URL (`?view=azloc-...`), the stable path is
listed and the redirect is noted. Re-verify before an audit submission — the
Architecture Center reorganises regularly.
{{% /alert %}}

## Patterns we cover

{{< cards >}}
{{% card title="Single-site multi-node cluster" href="https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-baseline" icon="settings" %}}
Standard datacentre pattern. Storage-switched, 2–16 validated nodes, dual ToR.
Covered by the Azure Local baseline reference architecture.
{{% /card %}}
{{% card title="Branch 2-node switchless" href="https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-switchless" icon="collections" %}}
Edge / branch pattern. 2–4 nodes, direct interlink storage cabling, cloud
witness. Suits dozens of low-VM-count sites.
{{% /card %}}
{{% card title="Single-node Azure Local (far edge)" href="https://learn.microsoft.com/en-us/azure/azure-local/plan/single-server-deployment" icon="document" %}}
Ruggedised single node for far-edge sites. No Architecture Center article —
the network reference pattern in the product docs is the official source.
{{% /card %}}
{{% card title="Multi-site resiliency" href="https://learn.microsoft.com/en-us/azure/azure-local/manage/disaster-recovery-workloads-resiliency" icon="share" %}}
Stretched clusters were removed in Azure Local 23H2. Multi-site DR is now
addressed at the workload layer.
{{% /card %}}
{{% card title="AKS on Azure Local" href="https://learn.microsoft.com/en-us/azure/architecture/example-scenario/hybrid/aks-baseline" icon="grid" %}}
Container platform on Azure Local via AKS enabled by Arc — for line-of-business
apps needing orchestration on-premises.
{{% /card %}}
{{% card title="Arc-enabled SQL MI" href="https://learn.microsoft.com/en-us/azure/architecture/hybrid/arc-sql-managed-instance-disaster-recovery" icon="collections" %}}
Managed SQL with Azure-style operations on Arc-enabled Kubernetes, with
two-site Business Critical failover.
{{% /card %}}
{{% card title="AVD on Azure Local" href="https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-workload-virtual-desktop" icon="person" %}}
Session hosts on Azure Local for edge latency or data-sovereignty desktop
requirements.
{{% /card %}}
{{% card title="Hybrid observability" href="https://learn.microsoft.com/en-us/azure/architecture/hybrid/hybrid-perf-monitoring" icon="flash" %}}
Azure Monitor and Log Analytics across on-premises, edge and Azure workloads.
{{% /card %}}
{{< /cards >}}

## Pattern selection grid

The customer's discovery answers map to a pattern as follows:

| Customer signal | Recommended starting pattern | Official architecture |
|---|---|---|
| One datacentre, refresh of 3-tier infra | Single-site multi-node cluster | [Azure Local baseline](https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-baseline) |
| Many branches, low VM count per site | Branch 2-node switchless | [Azure Local storage switchless](https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-switchless) |
| Far-edge, intermittent connectivity | Single-node Azure Local | [Single-server deployment pattern](https://learn.microsoft.com/en-us/azure/azure-local/plan/single-server-deployment) — product doc |
| Two paired datacentres, DR requirement | Workload-layer resiliency (not a stretched cluster) | [Workloads resiliency for Azure Local](https://learn.microsoft.com/en-us/azure/azure-local/manage/disaster-recovery-workloads-resiliency) — product doc |
| Container-first modern apps on-prem | AKS on Azure Local | [AKS baseline for Azure Local](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/hybrid/aks-baseline) |
| Sovereign SQL workload on-prem | Arc-enabled SQL MI | [Arc SQL MI disaster recovery](https://learn.microsoft.com/en-us/azure/architecture/hybrid/arc-sql-managed-instance-disaster-recovery) |
| Desktop estate with sovereignty or latency constraints | AVD on Azure Local | [AVD for Azure Local](https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-workload-virtual-desktop) |
| Existing VMware estate to be brought under Azure governance | Arc-enabled VMware vSphere | [Arc-enabled VMware vSphere overview](https://learn.microsoft.com/en-us/azure/azure-arc/vmware-vsphere/overview) — product doc |

## Verified Azure Architecture Center coverage

The audit asks you to demonstrate capability against recognised architectures.
This is the full set of official articles covering the technology in the
Module B checklist.

| # | Article | Type | Covers | Maps to |
|---|---|---|---|---|
| 1 | [Azure Local baseline reference architecture](https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-baseline) | Reference architecture | Workload-agnostic storage-switched multi-node design: S2D, Hyper-V, Network ATC, secured-core, Arc, Monitor, Defender, Update Manager | Single-site cluster; B.1.1 |
| 2 | [Azure Local storage switchless architecture](https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-switchless) | Reference architecture | 2-, 3- and 4-node edge/branch clusters using direct interlink cabling (retail, manufacturing, ROBO) | Branch switchless; B.1.1 |
| 3 | [AKS baseline architecture for AKS on Azure Local](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/hybrid/aks-baseline) | Example scenario (baseline) | AKS enabled by Arc on Azure Local — networking, security, identity, management, monitoring | AKS on Azure Local; B.1.1 |
| 4 | [Deploy and operate apps with AKS enabled by Arc on Azure Local](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/hybrid/aks-hybrid-azure-local) | Example scenario | Containerised application CI/CD on AKS on Azure Local using Arc and GitOps / Flux | AKS on Azure Local; B.4.2 |
| 5 | [Azure Arc-enabled SQL Managed Instance disaster recovery](https://learn.microsoft.com/en-us/azure/architecture/hybrid/arc-sql-managed-instance-disaster-recovery) | Example scenario | Arc SQL MI Business Critical across two sites on Arc-enabled Kubernetes with failover | Arc SQL MI; B.1.1 |
| 6 | [Administer SQL Server with Azure Arc](https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-arc-sql-server) | Reference architecture | Manage, maintain and monitor on-premises and multicloud SQL Server via Arc | Arc-enabled data services; B.1.1 |
| 7 | [Manage and deploy Kubernetes in Azure Arc](https://learn.microsoft.com/en-us/azure/architecture/hybrid/arc-hybrid-kubernetes) | Reference architecture | Arc-enabled Kubernetes cluster management and GitOps configuration across datacentre, edge and multicloud | Arc-enabled Kubernetes; B.1.1 |
| 8 | [Azure Virtual Desktop for Azure Local](https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-workload-virtual-desktop) | Example scenario | AVD session hosts on Azure Local for edge and data-sovereignty desktop estates | AVD on Azure Local; B.1.1 |
| 9 | [Monitor hybrid availability and performance](https://learn.microsoft.com/en-us/azure/architecture/hybrid/hybrid-perf-monitoring) | Reference architecture | Azure Monitor and Log Analytics for on-premises, other-cloud and Azure workloads | Hybrid observability; B.1.1 |
| 10 | [Architecture best practices for Azure Local](https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-local) | Well-Architected service guide | Five-pillar WAF guidance for Azure Local — reliability, security, cost, operations, performance | [WAF assessment](waf-assessment/); B.1.1 |
| 11 | [Azure hybrid options](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/hybrid-considerations) | Decision guide | Choosing between on-premises, edge, Azure and other-cloud hosting | Qualification; discovery |
| 12 | [Hybrid architecture design](https://learn.microsoft.com/en-us/azure/architecture/hybrid/hybrid-start-here) | Landing page | Curated index of hybrid and multicloud architectures | Navigation |

### Supporting product documentation

Where a capability in the Module B checklist has no Architecture Center
article, this is the official Microsoft source to cite instead.

| Technology | Official source | Why it is here rather than the Architecture Center |
|---|---|---|
| Single-node far edge | [Single-node network reference pattern](https://learn.microsoft.com/en-us/azure/azure-local/plan/single-server-deployment) | No Architecture Center article; the baseline covers 1–16 nodes but gives no single-node design |
| Network pattern selection | [Choose a network reference pattern](https://learn.microsoft.com/en-us/azure/azure-local/plan/choose-network-pattern) | Selector across single-node and two-node switched / switchless / converged patterns |
| Multi-site DR | [Workloads resiliency for Azure Local](https://learn.microsoft.com/en-us/azure/azure-local/manage/disaster-recovery-workloads-resiliency) | Stretched clusters were removed in Azure Local 23H2; DR is layered at the workload tier |
| S2D stretch / geo DR | [Disaster recovery for Storage Spaces Direct](https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/storage-spaces-direct-disaster-recovery) | Storage Replica options at the OS layer — closest analogue to the legacy stretched-cluster concept |
| Arc-enabled servers | [Azure Arc-enabled servers overview](https://learn.microsoft.com/en-us/azure/azure-arc/servers/overview) | Foundational for Monitor, Update Manager, Defender and Policy on non-Azure servers |
| Arc-enabled VMware vSphere | [Arc-enabled VMware vSphere overview](https://learn.microsoft.com/en-us/azure/azure-arc/vmware-vsphere/overview) | No dedicated Architecture Center article |
| Arc-enabled SCVMM | [Arc-enabled SCVMM overview](https://learn.microsoft.com/en-us/azure/azure-arc/system-center-virtual-machine-manager/overview) | No dedicated Architecture Center article |
| Arc SQL MI (product) | [SQL Managed Instance enabled by Azure Arc](https://learn.microsoft.com/en-us/azure/azure-arc/data/managed-instance-overview) | Concept overview to accompany the DR architecture above |
| Azure Local platform | [Azure Local overview](https://learn.microsoft.com/en-us/azure/azure-local/overview) | The Architecture Center has no Azure Local index page |

### Browse the catalogue yourself

| Filter | URL |
|---|---|
| Hybrid and multicloud architectures | <https://learn.microsoft.com/en-us/azure/architecture/browse/?azure_categories=hybrid> |
| Everything tagged Azure Local | <https://learn.microsoft.com/en-us/azure/architecture/browse/?products=azure-local> |

## Known gaps

Be explicit with the auditor about these — claiming an architecture that does
not exist is worse than naming the substitute you used.

| Required capability | Gap | What to cite instead |
|---|---|---|
| Single-node Azure Local | No Architecture Center article | The single-server network reference pattern, plus your own as-built diagram |
| Stretched cluster (multi-site) | Removed from the platform in Azure Local 23H2; no current architecture exists | Workloads resiliency guidance, Arc SQL MI two-site DR, or Storage Spaces Direct DR at the OS layer |
| Arc SQL MI *specifically on Azure Local* | The Arc SQL MI article targets generic Arc-enabled Kubernetes, not Azure Local by name | Combine the Arc SQL MI DR architecture with the AKS-on-Azure-Local baseline |
| GPU / AI at the edge | No dedicated article | AKS-on-Azure-Local baselines (GPU node pools) plus the Azure Local WAF service guide |
| Entra hybrid join, BitLocker, WDAC, sovereignty | No standalone article | The security sections of the Azure Local baseline and the WAF service guide |

## Decision inputs

| # | Input | Why it matters |
|---|---|---|
| 1 | Site count + per-site host count | Drives switchless vs. switched, cluster size |
| 2 | RPO / RTO per workload tier | Drives workload-layer DR design (stretch is no longer available) |
| 3 | Workload profile (VM / container / SQL / desktop) | Drives AKS, Arc-SQL or AVD add-ons |
| 4 | Connectivity per site | Drives witness choice + Arc proxy config |
| 5 | Regulatory drivers | Drives secured-core + WDAC + sovereignty patterns |

## Output: customer-ready deliverable

A one-page pattern-selection memo cross-referenced to the HLD. Each selected
pattern in the [HLD](deliverables/hld-template/) must cite the matching article
URL from the table above — that citation is what turns a diagram into audit
evidence.

{{% alert type="caution" %}}
This repo intentionally does **not** redraw diagrams. The Azure Architecture
Center diagrams change frequently; copying them creates drift. Link to the live
URL and embed only customer-specific overlays.
{{% /alert %}}

## Reuse & contribute back

{{% alert type="tip" %}}
If you delivered a variant the tables don't cover, open a PR adding a card, a
row to the selection grid, and — if it closes one of the known gaps above — a
note saying which official article now covers it.
{{% /alert %}}

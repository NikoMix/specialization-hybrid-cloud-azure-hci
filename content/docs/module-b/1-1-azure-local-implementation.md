---
title: "B.1.1 – Azure Local Implementation Capability"
description: "Evidence requirements for control B.1.1 – technical capability to design, deploy, and operate hybrid infrastructure on Microsoft Azure Local."
linkTitle: "1.1 Azure Local Implementation"
weight: 1
---

{{% alert type="caution" %}}
**`TODO: verify against spec PDF`** — confirm the exact number of required customer deployments,
the recency window, and any specific architecture artefacts mandated by the current
Microsoft-issued *Hybrid Cloud Infrastructure with Microsoft Azure Local Advanced Specialization*
requirements document.
{{% /alert %}}

## What the Auditor Checks

The auditor verifies that your organisation has **demonstrated technical capability** in designing, deploying, and operating Microsoft Azure Local clusters (and the surrounding Azure Arc / hybrid management stack) for real customers — not just knowledge, but practical delivery experience on validated hardware platforms.

**Typical questions:**
- Can you demonstrate Azure Local cluster deployments completed for real customers?
- What validated hardware platforms (Dell, HPE, Lenovo, etc.) has your team deployed?
- Do you have reference architectures, deployment runbooks, and operational handover assets?
- Are deployed clusters registered to Azure and Arc-enrolled, with observability and protection wired up?

---

## Required Evidence Checklist

| # | Evidence Item | Accepted Formats | Status |
|---|---|---|---|
| 1 | **Solution case studies** (at least 2 Azure Local / hybrid focused) | PDF, PowerPoint | ⬜ |
| 2 | **Architecture diagrams** for delivered Azure Local clusters (nodes, network, Arc, observability) | PDF, Visio, Draw.io | ⬜ |
| 3 | **Bill of materials (BoM)** for at least one validated hardware platform | PDF, Excel | ⬜ |
| 4 | **Deployment runbook or as-built document** from a real engagement (anonymised) | PDF, Word | ⬜ |
| 5 | **Service capability statement** listing Azure Local / Arc capabilities your team delivers | PDF, Word | ⬜ |
| 6 | **Azure resource list** — Azure Local clusters, Arc-enabled resources, and connected services (with customer mapping) | PDF, Excel | ⬜ |

{{% alert type="tip" %}}
Case studies should explicitly reference Azure Local (or "Azure Stack HCI" for older deployments)
and the Arc-enabled services in scope (e.g. Arc-enabled servers, Arc-enabled Kubernetes, Azure
Monitor, Azure Backup, Azure Site Recovery, AKS hybrid). Generic "on-prem virtualisation"
descriptions without explicit Azure service references are weak evidence.
{{% /alert %}}

---

## Evidence Guidance

### Case Study Structure

Each case study should include:

```markdown
## Customer: [Customer A / Full name with consent]
**Industry:** [e.g., Manufacturing, Public Sector, Retail]
**Challenge:** [Brief description of the business problem — typically refresh of
  ageing 3-tier infrastructure, edge consolidation, sovereign workload hosting,
  disconnected site, or VMware migration]
**Solution:**
- Hardware: [e.g., 4-node Dell Integrated System for Azure Local AX-650]
- Topology: [e.g., switchless storage, dual-ToR network, stretched cluster
  across two sites with site-aware fault domains]
- Azure services used: [Azure Local, Arc-enabled servers, Arc-enabled
  Kubernetes, Azure Monitor, Log Analytics, Azure Backup, Azure Site Recovery]
- Workloads on cluster: [Hyper-V VMs, AKS hybrid clusters, SQL Server,
  Windows Admin Center management]
**Outcome:**
- Business outcome: [e.g., consolidated 14 ageing hosts into 4 nodes,
  60% datacentre footprint reduction]
- Technical metrics: [e.g., RPO 1h via ASR, RTO 30min, monthly patching
  via Azure Update Manager]
**Delivery timeline:** [e.g., 8 weeks from kickoff to go-live]
**Your team's role:** [Lead architect + delivery / Implementation partner]
```

### Architecture Diagrams

Diagrams should clearly show:
- **Physical layer:** node count, validated hardware SKU, switch topology (ToR, storage fabric)
- **Network design:** management / storage / compute VLANs, RDMA / SET teaming, ATC intent (if used)
- **Storage layer:** Storage Spaces Direct (S2D) volumes, ReFS, resiliency tier, deduplication
- **Compute layer:** Hyper-V hosts, VM tiers, AKS hybrid (if used), GPU partitioning (if applicable)
- **Azure plane:** Azure Local resource, Arc enrolment, Azure Monitor, Backup, Site Recovery, Update Manager
- **Identity & security:** Entra ID Hybrid Join, local AD, secured-core, BitLocker, Microsoft Defender for Cloud

**Tools:** Microsoft Visio, draw.io, Lucidchart, Azure Architecture Center templates for Azure Local.

{{% alert type="tip" title="Anchor every diagram to a published Microsoft architecture" %}}
The auditor can check a delivered design against a Microsoft-published
reference far more easily than against a bespoke drawing. The
[reference architectures page](/docs/engagement/reference-architectures/) maps
each delivery pattern to its verified Azure Architecture Center article — for
example the [Azure Local baseline](https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-baseline)
for a storage-switched multi-node cluster, or the
[storage switchless architecture](https://learn.microsoft.com/en-us/azure/architecture/hybrid/azure-local-switchless)
for a 2-node branch build. Cite the URL on the diagram itself.

It also records the gaps: there is **no** Architecture Center article for a
single-node far-edge deployment, and stretched clusters were removed from the
platform in Azure Local 23H2. If you delivered either, say so explicitly and
cite the product documentation instead of implying an architecture that does
not exist.
{{% /alert %}}

### Bill of Materials (BoM)

Provide a BoM for at least one delivered cluster. Acceptable formats include the validated hardware vendor's quote sheet, an Azure Local "Sizer" export, or a tabulated configuration sheet. Must include:
- Cluster name (anonymised) and number of nodes
- Node SKU (must be on the Azure Local validated catalogue) — e.g. *Dell AX-650*, *HPE ProLiant DL360 Gen11 for Azure Local*, *Lenovo ThinkAgile MX*
- CPU / memory / disk (cache + capacity) per node
- Network adapters and switch fabric
- Software stack: Azure Local OS version, Windows Server datacenter licensing, SQL/AKS as applicable

### Capability Statement

A 1–2 page document listing:
- Azure Local / Arc capabilities your team is qualified to deliver
- Number of completed clusters per validated hardware vendor
- Key team members and their relevant certifications (AZ-800, AZ-801, AZ-104, AZ-305, vendor certs)
- Microsoft partner competencies and designations

---

## Azure Local & Arc Services Reference

Evidence should cover services from the eligible hybrid pillars:

| Pillar | Key Services |
|---|---|
| Azure Local platform | Azure Local instances, S2D storage, Hyper-V, Network ATC, secured-core |
| Azure Arc – compute | Arc-enabled servers, Arc-enabled VMware vSphere, Arc-enabled SCVMM, AKS enabled by Arc |
| Azure Arc – data | Arc-enabled SQL Managed Instance, Arc-enabled PostgreSQL, Arc-enabled SQL Server |
| Hybrid resiliency | Azure Backup (MARS / MABS), Azure Site Recovery |
| Hybrid observability & ops | Azure Monitor, Log Analytics, Azure Update Manager, Microsoft Defender for Cloud, Windows Admin Center |
| Hybrid containers | AKS hybrid / AKS enabled by Arc, Kubernetes extensions via Arc |

---

## Evidence Status

| Evidence Item | Owner | Due Date | Status | Notes |
|---|---|---|---|---|
| Case study 1 | | | ⬜ | |
| Case study 2 | | | ⬜ | |
| Architecture diagram 1 | | | ⬜ | |
| Architecture diagram 2 | | | ⬜ | |
| Bill of materials | | | ⬜ | |
| Deployment runbook / as-built | | | ⬜ | |
| Capability statement | | | ⬜ | |

---

## Common Gaps

| Gap | Remediation |
|---|---|
| Case studies describe "on-prem virtualisation" without naming Azure Local / Arc | Rewrite or annotate to explicitly list Azure Local, the Arc services in scope, and the cluster resource ID |
| Hardware used was not on the Azure Local validated catalogue | Document the validated SKU explicitly; if a customer used non-validated hardware, do not submit that engagement |
| No Arc-enrolment evidence | Capture an Azure portal screenshot of the cluster resource + Arc-enabled servers under the customer's tenant (redact tenant IDs) |
| Architecture diagrams are high-level only | Add a detailed view showing storage network, switch topology, and the Azure services connected to the cluster |
| No referenceable customer outcomes | Use internally measurable outcomes (e.g. host consolidation ratio, RPO/RTO improvement, datacentre footprint reduction) if customer KPIs aren't available |

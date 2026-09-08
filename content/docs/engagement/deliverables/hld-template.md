---
title: "Deliverable – High-Level Design (HLD) Template"
description: "HLD template tailored to an Azure Local + Arc engagement."
linkTitle: "HLD template"
weight: 1
---

## When to use this

Output of the design phase, ahead of LLD. The HLD is the document the
customer's architecture review board signs off; it must be readable by a
non-Azure-Local reader.

{{< button href="templates/deliverables/hld-template.docx" icon="document" >}}Download hld-template.docx{{< /button >}}

## Inputs you need from the customer

| # | Input | Source | Format |
|---|---|---|---|
| 1 | Discovery workbook | Discovery workshop | Spreadsheet |
| 2 | WAF assessment | WAF workshop | Spreadsheet |
| 3 | Assessment platform outputs | MAP / Azure Migrate / Arc readiness | Multiple |
| 4 | Workload tiering & RPO/RTO | Discovery | Table |
| 5 | Selected reference architecture | Pattern selection memo | Document |

## Section outline (matches the workfile)

1. Executive summary
2. Business outcomes & success criteria
3. Solution overview (selected pattern + Azure Architecture Center link)
4. Physical architecture (sites, nodes, switches, BoM summary)
5. Network design (intents, VLANs, RDMA, ToR, Arc connectivity)
6. Storage design (S2D volumes, tiers, resiliency, BitLocker)
7. Compute design (Hyper-V, AKS on Azure Local if in scope)
8. Azure plane (Arc, Monitor, Defender, Update Manager, Backup, Site Recovery)
9. Identity & access (Entra ID, Arc RBAC, local AD)
10. Security posture (secured-core, WDAC, microsegmentation)
11. DR design (witness, stretch, ASR, backup tiering)
12. Operations model (who runs it, change & patch cadence)
13. Risks & assumptions (linked to WAF + decision log)
14. Roadmap (post-go-live add-ons: AKS, Arc-SQL, stretch)
15. Appendices (workbooks, raw assessment exports)

## Step-by-step

1. Open the workfile and fill the executive summary against the customer's
   stated outcomes.
2. Paste the selected reference-architecture link and customer-specific
   overlay diagram.
3. Carry forward the WAF top-10 recommendations into Section 13 (Risks).
4. Review with the customer's architecture lead before LLD kickoff.

## Reuse & contribute back

{{% alert type="tip" %}}
If you keep adding the same section that isn't in the template, open a PR
promoting it into the default outline.
{{% /alert %}}

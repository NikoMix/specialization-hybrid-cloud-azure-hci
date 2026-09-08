---
title: "Engagement – Microsoft Assessment Platform Inputs"
description: "How to feed Microsoft assessment tooling (MAP, Azure Migrate, Cloud Adoption Strategy, Azure Arc readiness) for an Azure Local engagement."
linkTitle: "5 · Assessment platforms"
weight: 5
---

## When to use this

In parallel with the discovery workshop and WAF assessment. The output from
these Microsoft platforms becomes evidence in Module B (capability) and
informs the BoM and Arc rollout plan.

{{< button href="templates/engagement/assessment-platform-inputs.xlsx" icon="document" >}}Download assessment-platform-inputs.xlsx{{< /button >}}

## Platforms in scope

| Platform | Purpose for an Azure Local engagement |
|---|---|
| Microsoft Assessment and Planning Toolkit (MAP) | Current-state inventory of Windows hosts, SQL, Hyper-V — feeds workload tiering. |
| Azure Migrate (appliance) | Discovery + dependency analysis for workloads candidate for Azure Local. |
| Cloud Adoption Strategy Evaluator | Surfaces governance, landing zone, and operating-model gaps. |
| **Azure Arc readiness assessment** | Confirms which existing servers, K8s clusters, and SQL estates can be Arc-enrolled and what blocks them. |
| Azure Local Sizer | Validates BoM against workload profile from MAP / Azure Migrate. |

## Required inputs per platform

The workbook has a tab per platform with the exact fields the customer
needs to supply.

| # | Input | Source | Format |
|---|---|---|---|
| 1 | Windows / Linux host inventory with CPU / RAM / disk | MAP export | CSV |
| 2 | Hyper-V / VMware VM inventory with utilisation | Azure Migrate appliance | Azure Migrate project |
| 3 | SQL Server inventory + edition + version | MAP / Azure Migrate | Spreadsheet |
| 4 | Network bandwidth + latency per site | Customer network team | Table |
| 5 | Tenant + subscription + landing-zone status | Cloud lead | Free text |
| 6 | List of servers / clusters in scope for Arc | Cloud lead | List |

## Step-by-step

1. Deploy the Azure Migrate appliance to the source environment (or reuse
   an existing one).
2. Run MAP if no Azure Migrate is available, or to enrich SQL discovery.
3. Run the Azure Arc readiness assessment for the in-scope server and K8s
   estates; capture blockers (OS version, connectivity, proxy, identity).
4. Feed the consolidated dataset into the Azure Local Sizer to validate the
   BoM long-list from the discovery workshop.
5. Run the Cloud Adoption Strategy Evaluator with the customer's exec
   sponsor; record gaps that become risks in the project plan.
6. Archive all assessment exports in the engagement evidence pack — this
   is Module B.1.1 capability evidence for the audit.

## Output: customer-ready deliverable

A consolidated `assessment-platform-inputs.xlsx` plus the raw exports from
each platform, attached as an appendix to the HLD.

## Reuse & contribute back

{{% alert type="tip" %}}
Found a recurring blocker in the Arc readiness assessment (e.g. a missing
TLS root, a proxy quirk)? Open a `lesson-learned` issue so the next
consultant catches it earlier.
{{% /alert %}}

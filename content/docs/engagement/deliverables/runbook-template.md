---
title: "Deliverable – Cluster Lifecycle Runbook Template"
description: "Day-1 to day-2 operational runbook covering Azure Local cluster build, validation, patching, scaling, and decommission."
linkTitle: "Runbook template"
weight: 3
---

## When to use this

Created during build, updated through hypercare, handed to customer ops at
KT. This is the **single source of truth** for cluster operations — most
audit findings for B.4.2 stem from a missing or stale runbook.

{{< button href="templates/deliverables/runbook-template.docx" icon="document" >}}Download runbook-template.docx{{< /button >}}

## Inputs you need from the customer

| # | Input | Source | Format |
|---|---|---|---|
| 1 | Signed-off LLD | Design phase | Document |
| 2 | Customer change-management policy | Ops team | Document |
| 3 | Patch maintenance window | Ops team | Schedule |
| 4 | Escalation contacts | Ops team | List |
| 5 | Vendor support contracts | Procurement | Contracts |

## Section outline (matches the workfile)

### Day 0 – Build & commission

1. Pre-checks (firmware baseline, BIOS settings, BMC / iLO / iDRAC)
2. Network ATC deployment + validation
3. Cluster creation + Storage Spaces Direct enablement
4. Azure Local registration to Azure
5. Witness configuration
6. Post-build validation tests with expected output

### Day 1 – Workload onboarding

7. VM placement & live-migration policy
8. AKS on Azure Local enablement (if in scope)
9. Arc enrolment for guest workloads
10. Backup policy assignment
11. Site Recovery enablement (if in scope)

### Day 2 – Steady-state operations

12. Monitoring & alerting playbook (top 20 alerts, who responds, SLA)
13. Patching cycle — firmware, drivers, OS, Azure Local solution updates
14. Capacity management thresholds
15. Adding / removing a node
16. Volume resize / rebalance
17. Witness failure recovery
18. Stretch failover & failback drill
19. Certificate rotation

### Lifecycle events

20. Annual DR drill
21. Hardware refresh planning
22. Decommission & secure data destruction

## Step-by-step

1. Start the runbook from this template at the build phase, not at handover.
2. Capture as-built values inline (cluster name, witness path, etc).
3. Every operational change during build / hypercare must update the
   matching runbook section.
4. KT signs off the runbook with customer ops; sign-off is part of the
   Definition of Done.

## Reuse & contribute back

{{% alert type="tip" %}}
If you ran a steady-state op that isn't in the runbook (e.g. emergency
spare-node swap), open a PR adding it as a new section.
{{% /alert %}}

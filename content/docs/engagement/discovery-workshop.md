---
title: "Engagement – Discovery Workshop Kit"
description: "1-day discovery workshop agenda, deck, and workbook for an Azure Local hybrid-infrastructure engagement."
linkTitle: "3 · Discovery workshop"
weight: 3
---

## When to use this

After the qualification questionnaire has scored mostly green and the
customer has agreed to invest a day. Discovery is the foundation for the
HLD; cutting it short usually shows up later as scope creep.

{{< button href="templates/engagement/discovery-workshop-deck.pptx" icon="document" >}}Download discovery-workshop-deck.pptx{{< /button >}}

{{< button href="templates/engagement/discovery-workshop-workbook.xlsx" icon="document" >}}Download discovery-workshop-workbook.xlsx{{< /button >}}

## Inputs you need from the customer

| # | Input | Source | Format |
|---|---|---|---|
| 1 | Completed qualification questionnaire | Account team | Document |
| 2 | Current-state architecture diagrams | Infra lead | PDF / Visio |
| 3 | Workload inventory with criticality + RPO/RTO | App owners | Spreadsheet |
| 4 | Existing monitoring & backup runbook excerpts | Ops lead | Document |
| 5 | List of regulatory / compliance controls in scope | CISO / DPO | List |

## Default 1-day agenda

| Time | Topic | Outcome |
|---|---|---|
| 09:00 | Welcome + outcomes alignment | Shared goals + decision rights |
| 09:30 | Current-state review | Captured topology + pain points |
| 10:30 | Target hybrid pattern selection | Single-site / branch / stretch / edge |
| 11:30 | Workload-to-cluster placement | Workload table sorted by tier |
| 13:30 | Validated hardware shortlist | BoM long-list with two vendor options |
| 14:30 | Arc & observability target state | Arc scope, monitoring + SIEM plan |
| 15:30 | DR & backup target state | RPO / RTO per workload tier |
| 16:30 | Risks, dependencies, next-step decisions | Decision log + draft HLD scope |

## Step-by-step

1. Send the workbook 48 hours ahead so the customer can pre-populate the
   workload inventory and current-state diagrams.
2. Open with outcomes + decision rights; confirm who can sign off on the
   target architecture.
3. Walk the deck section by section, capturing answers in the workbook tabs
   (`Current state`, `Target state`, `Workloads`, `Risks`).
4. Close with three concrete decisions captured in the workbook decision
   log.
5. Within 5 business days send the discovery report (workbook + annotated
   deck + a draft HLD scope statement).

## Output: customer-ready deliverable

A completed discovery workbook, an annotated workshop deck, and a draft HLD
scope statement. These feed directly into the HLD template.

## Reuse & contribute back

{{% alert type="tip" %}}
Did a workshop section run long or short? Adjust the timing column and
open a PR — every engagement should sharpen the default agenda.
{{% /alert %}}

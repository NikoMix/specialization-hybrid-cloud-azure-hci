---
title: "Deliverable – Hypercare Plan Template"
description: "4-week (default) hypercare plan for an Azure Local cluster post go-live."
linkTitle: "Hypercare plan template"
weight: 5
---

## When to use this

Activated at cutover. Hypercare is the structured handhold period where
the partner owns operations jointly with the customer before a hard exit.

{{< button href="templates/deliverables/hypercare-plan-template.docx" icon="document" >}}Download hypercare-plan-template.docx{{< /button >}}

## Inputs you need from the customer

| # | Input | Source | Format |
|---|---|---|---|
| 1 | Go-live date | Project plan | Date |
| 2 | Ops shift roster | Ops lead | Schedule |
| 3 | Incident priority matrix | ITSM | Table |
| 4 | On-call partner contacts | Partner delivery | List |
| 5 | Exit-criteria sign-off authority | Steering committee | Named person |

## Default 4-week hypercare structure

| Week | Partner role | Customer role | Exit gate |
|---|---|---|---|
| 1 | Lead all ops + shadow customer | Shadow + observe | First patch cycle executed jointly |
| 2 | Joint ops + handover runbooks | Joint ops | Backup restore test signed off |
| 3 | Customer leads; partner safety net | Lead all ops | Top 10 day-2 ops performed by customer |
| 4 | On-call only | Lead all ops + first DR drill | Final review + DoD sign-off |

## Cadences

| Cadence | Attendees | Purpose |
|---|---|---|
| Daily stand-up (week 1–2) | Partner + customer ops | Triage, blockers |
| Twice-weekly stand-up (week 3–4) | Partner + customer ops | Steady state |
| Weekly health review | Partner lead + customer ops lead | Metrics, risks |
| Final review | Partner + customer steering | DoD sign-off |

## Step-by-step

1. Activate the hypercare plan at cutover; cancel any other partner
   commitments that would compete with on-call.
2. Run the cadence above; capture every incident in the customer's ITSM
   plus a copy in the engagement evidence pack.
3. At end of week 4 hold the final review and walk the Definition of Done.
4. Close the engagement; raise the lessons-learned issue.

## Reuse & contribute back

{{% alert type="tip" %}}
If your customer needed a longer hypercare (e.g. multi-site rollouts),
extend the table and open a PR with a new default variant.
{{% /alert %}}

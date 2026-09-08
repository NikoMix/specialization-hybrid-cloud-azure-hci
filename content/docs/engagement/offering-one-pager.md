---
title: "Engagement – Offering One-Pager"
description: "Productised Azure Local + Arc managed-platform offering — what we sell, to whom, for how much, with what outcome."
linkTitle: "1 · Offering one-pager"
weight: 1
---

## When to use this

Before the first qualification conversation with a prospect. The one-pager
gives sales, presales, and the customer's IT lead a shared picture of what
the engagement is and what it costs.

{{< button href="templates/engagement/offering-one-pager.pptx" icon="document" >}}Download offering-one-pager.pptx{{< /button >}}

## Inputs you need from the customer

| # | Input | Source | Format |
|---|---|---|---|
| 1 | Number of datacentre + edge / branch sites | IT inventory | Number |
| 2 | Current hypervisor and refresh window | CIO / Infra lead | Free text |
| 3 | Regulatory / sovereignty drivers | CISO / DPO | Free text |
| 4 | Existing Azure footprint and Arc usage | Cloud team | Free text |
| 5 | Target go-live for first cluster | Steering committee | Date |

## Productised offering — default shape

The default offering is **"Azure Local Managed Platform – first-cluster
landing zone"**: one production cluster on validated hardware, Arc-enrolled,
with observability, backup, and update management wired up, plus a 4-week
hypercare and a KT package.

### Scope (in)

- Discovery workshop (1 day, on-site or remote)
- HLD and LLD (using the templates in this repo)
- Validated-hardware BoM and vendor coordination
- Cluster build on one site (2-node switchless or 4–16 node aggregation)
- Arc enrolment for the cluster and its in-scope workloads
- Azure Monitor / Defender for Cloud / Update Manager / Backup wiring
- 4 weeks of hypercare with weekly health reviews
- Operations runbook + KT to customer ops

### Scope (out)

- Application migration / refactor (separate engagement)
- AKS on Azure Local (add-on module — see reference architectures)
- Multi-site stretch / DR (add-on module)
- Long-term managed-service operations (separate MSA)

## Outcomes (Definition of Done — summary)

Full Definition of Done lives on the dedicated page. Headline outcomes:

- Cluster healthy in Azure portal and Windows Admin Center
- Arc-enabled and visible under the customer tenant
- Monitoring, backup, and DR tested end-to-end
- Operations runbook signed off by customer ops
- Audit-grade evidence pack added to this repo for the customer engagement

## Indicative commercials

| Tier | Cluster size | Indicative duration | Indicative fee band |
|---|---|---|---|
| Edge / branch | 2 node switchless | 4–6 weeks | $$ |
| Standard datacentre | 4–8 node | 6–10 weeks | $$$ |
| Aggregation / sovereign | 8–16 node + stretch | 10–14 weeks | $$$$ |

{{% alert type="caution" %}}
Replace the indicative bands with your local rate-card before sending to a
prospect. Bands shown above are placeholders.
{{% /alert %}}

## Step-by-step (how the offering is delivered)

1. Qualify (this page + qualification questionnaire)
2. Discovery workshop + WAF + MAP / Arc readiness
3. HLD + LLD + BoM sign-off
4. Hardware procurement and rack-and-stack
5. Cluster deploy, Arc enrol, observability + backup + DR wiring
6. Hypercare + KT
7. Definition of Done sign-off + innersource lessons-learned PR

## Reuse & contribute back

{{% alert type="tip" %}}
Customised the one-pager for a vertical (manufacturing, public sector,
retail)? Open a PR adding a variant slide, or raise an issue with the
`innersource` + `engagement-playbook` labels.
{{% /alert %}}

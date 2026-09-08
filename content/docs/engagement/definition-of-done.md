---
title: "Engagement – Definition of Done"
description: "The exit checklist that closes an Azure Local engagement and triggers commercial sign-off and audit-evidence capture."
linkTitle: "8 · Definition of done"
weight: 8
---

## When to use this

At the end of build + before hypercare exit. The Definition of Done is a
hard gate: until every item is checked, the engagement is not closed and
the customer should not be billed the final milestone.

{{< button href="templates/engagement/definition-of-done.docx" icon="document" >}}Download definition-of-done.docx{{< /button >}}

## Inputs you need from the customer

| # | Input | Source | Format |
|---|---|---|---|
| 1 | Customer ops sign-off authority | Steering committee | Named person |
| 2 | Customer security sign-off authority | CISO delegate | Named person |
| 3 | Hypercare exit date | Project plan | Date |

## The checklist

### Cluster health

- [ ] All nodes report `Healthy` in Azure portal and Windows Admin Center
- [ ] Cluster validation report passes with no errors or warnings
- [ ] Storage Spaces Direct shows expected resiliency and headroom
- [ ] Witness is configured and reachable

### Arc enrolment

- [ ] Azure Local resource visible in the customer tenant
- [ ] Arc-enabled servers / K8s / data resources visible in the customer tenant
- [ ] RBAC roles assigned and tested
- [ ] Tags applied per the customer's tagging policy

### Observability

- [ ] Azure Monitor metrics flowing for the cluster and guest VMs
- [ ] Log Analytics workspace receiving Windows Event + Defender logs
- [ ] Alert rules deployed for at least: node down, S2D degraded, update
  required, certificate expiring
- [ ] Customer dashboards delivered and shown to ops team

### Backup & DR

- [ ] Azure Backup configured for in-scope guest VMs
- [ ] Restore test completed and signed off
- [ ] Site Recovery (if in scope) failover drill completed
- [ ] RPO / RTO results documented against the HLD targets

### Security

- [ ] Secured-core posture verified
- [ ] Defender for Servers / Containers enabled and at expected coverage
- [ ] BitLocker on S2D volumes enabled and keys escrowed per policy
- [ ] Application control (WDAC) policy mode confirmed with the customer

### Update management

- [ ] Azure Update Manager configured with the agreed cadence
- [ ] First patch cycle executed under partner supervision
- [ ] Customer ops team has run a patch cycle solo (KT proof point)

### Knowledge transfer

- [ ] Operations runbook delivered and walked through
- [ ] KT plan completed — every session signed off
- [ ] Customer ops team can perform the top 10 day-2 operations unaided

### Audit evidence (this repo)

- [ ] Anonymised case study added to the engagement evidence pack
- [ ] Architecture diagrams added (physical + logical + Azure plane)
- [ ] BoM added (validated SKU only)
- [ ] Cluster lifecycle runbook added (as-built version)
- [ ] Evidence mapped to Module B.1.1 in the evidence tracker

### Innersource (this repo)

- [ ] Lessons-learned issue raised
- [ ] Any template diffs opened as PRs
- [ ] Reference-architectures page updated if a new variant was delivered

## Sign-off

The Definition of Done is signed by:

| Role | Name | Date |
|---|---|---|
| Customer operations lead | | |
| Customer security lead | | |
| Partner delivery lead | | |
| Partner practice lead | | |

## Reuse & contribute back

{{% alert type="tip" %}}
Did you skip an item because it didn't apply, or did you add a new one
for this customer? Open a PR generalising the change.
{{% /alert %}}

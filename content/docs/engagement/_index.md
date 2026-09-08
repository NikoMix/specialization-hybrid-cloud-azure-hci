---
title: "Engagement Playbook"
description: "How to discover, sell, deliver, and hand over a Microsoft Azure Local (Azure Stack HCI) hybrid-infrastructure engagement end to end."
linkTitle: "Engagement playbook"
lede: "Turn the audit content in Modules A and B into a repeatable, productised offering."
weight: 60
---

The engagement playbook turns the audit content in Modules A and B into a
repeatable, productised offering — so a consultancy that has never delivered
an Azure Local cluster can run a credible engagement using the artefacts in
this section.

## Phases at a glance

{{< cards >}}
{{% card title="1 · Qualify" href="docs/engagement/offering-one-pager/" icon="checkmark" %}}
Offering one-pager + qualification questionnaire to confirm fit and
decide whether to invest in discovery.
{{% /card %}}
{{% card title="2 · Discover" href="docs/engagement/discovery-workshop/" icon="search" %}}
1-day discovery workshop, MAP / Azure Migrate / Arc readiness inputs,
and Well-Architected Framework assessment focused on Reliability,
Operational Excellence, and Security.
{{% /card %}}
{{% card title="3 · Design" href="docs/engagement/reference-architectures/" icon="grid" %}}
Reference architecture selection, HLD and LLD using the deliverable
templates, BoM against the Azure Local validated hardware catalog.
{{% /card %}}
{{% card title="4 · Build" href="docs/engagement/deliverables/runbook-template/" icon="flash" %}}
Cluster lifecycle runbook drives deploy, Arc enrolment, observability,
backup, and DR wiring.
{{% /card %}}
{{% card title="5 · Hand over" href="docs/engagement/deliverables/kt-plan-template/" icon="book" %}}
KT plan + hypercare plan templates; definition of done signed by
customer and partner.
{{% /card %}}
{{% card title="6 · Innersource" href="docs/innersource/contributing/" icon="github" %}}
Every engagement contributes lessons learned and template diffs back to
this repo via the `innersource` issue templates.
{{% /card %}}
{{< /cards >}}

## How to use this section

Read the pages in sidebar order on your first engagement. From the second
engagement onward, jump to the section that matches the current phase and
use the downloadable workfile linked in each page.

{{% alert type="tip" %}}
Every page has a **Download the workfile** button — those Word / PowerPoint
/ Excel files are the artefacts you customise per customer. The page
is the **method**; the workfile is the **deliverable**.
{{% /alert %}}

## WAF pillars to emphasise for Azure Local

Azure Local engagements consistently surface the same three pillars as
top-priority. The WAF assessment page goes deep on each one.

| Pillar | Why it matters most for Azure Local |
|---|---|
| Reliability | Cluster quorum, witness placement, stretch-cluster RPO/RTO, validated hardware refresh cadence. |
| Operational Excellence | Arc-driven inventory, Azure Update Manager cadence, Azure Policy guest configuration, ATC network intents. |
| Security | Secured-core servers, Defender for Servers / Containers, application control (WDAC), BitLocker on S2D volumes, RBAC via Arc. |

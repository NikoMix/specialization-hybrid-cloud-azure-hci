---
title: "B.2.2 – Customer Diversity"
description: "Evidence requirements for control B.2.2 – at least three unique customers contributing eligible Azure Local / hybrid infrastructure ACR."
linkTitle: "2.2 Customer Diversity"
weight: 3
---

{{% alert type="caution" %}}
**`TODO: verify against spec PDF`** — confirm the exact minimum unique customer count (3 is
typical for Infrastructure-track Advanced Specializations, but the *Hybrid Cloud Infrastructure
with Microsoft Azure Local* spec may differ) with your PDM or the current Microsoft-issued spec.
{{% /alert %}}

## What the Auditor Checks

The auditor verifies that your organisation has **at least three unique customers** contributing to qualifying ACR from the eligible Azure Local and hybrid infrastructure services within the measurement window — demonstrating breadth of customer reach, not just depth with a single client.

**Typical questions:**
- How many unique customers contribute to your qualifying ACR?
- Are they using eligible association types (DPOR, PAL, CSP)?
- Can you demonstrate diversity across industries or workload types?

---

## Required Evidence Checklist

| # | Evidence Item | Accepted Formats | Status |
|---|---|---|---|
| 1 | **Customer list with ACR contributions** — at least 3 unique customers | Excel, PDF | ⬜ |
| 2 | **Association type evidence per customer** — DPOR, PAL, or CSP | PDF, Screenshots | ⬜ |
| 3 | **Eligible service alignment per customer** — which Azure Local / Arc / hybrid service each customer contributes through | Excel, PDF | ⬜ |

{{% alert type="note" %}}
**Eligible Association Types:**
- Digital Partner of Record (DPOR)
- Partner Admin Link (PAL)
- Cloud Solution Provider (CSP)
{{% /alert %}}

---

## Eligible Service Categories

A customer counts toward the diversity requirement if they contribute eligible ACR through **any** of the following:

| Category | Eligible Services |
|---|---|
| Azure Local platform | Azure Local instances, Azure Stack HCI billing meters |
| Azure Arc | Arc-enabled servers, Arc-enabled Kubernetes / AKS hybrid, Arc-enabled data services |
| Hybrid resiliency | Azure Backup, Azure Site Recovery |
| Hybrid observability & ops | Azure Monitor, Log Analytics, Azure Update Manager, Defender for Cloud (verify scope) |

---

## Customer Diversity Mapping Table

Prepare and submit this table as evidence:

| Customer ID | Industry | Association Type | Azure Local? | Arc Services Used | Hybrid Resiliency Used | ACR Contribution (USD) |
|---|---|---|---|---|---|---|
| Customer A | Manufacturing | PAL | 4-node cluster | Arc-enabled servers, AKS hybrid | Azure Backup, ASR | $X,XXX |
| Customer B | Public Sector | DPOR | 2-node stretched cluster | Arc-enabled servers, Defender for Cloud | Azure Backup | $X,XXX |
| Customer C | Retail / Edge | CSP | — | Arc-enabled servers across 35 sites | Azure Backup | $X,XXX |
| **Minimum: 3 rows** | | | | | | |

{{% alert type="tip" %}}
Anonymise the table for the audit submission (Customer A, B, C) unless the auditor has confirmed
they will cross-check with Microsoft Partner Center data directly.
{{% /alert %}}

---

## How to Identify Unique Customer Contributions

1. In Partner Center → Insights → Azure Revenue, switch to the **"By Customer"** view
2. Filter by the spec's measurement window (typically last 12 months)
3. Identify customers contributing ACR in the eligible service categories listed above
4. Cross-reference with your DPOR / PAL / CSP association records

{{% alert type="caution" %}}
If a customer has revenue under multiple association types, they still count as **one unique
customer**. Likewise, a customer contributing across multiple categories counts as one.
{{% /alert %}}

---

## Evidence Status

| Evidence Item | Owner | Due Date | Status | Notes |
|---|---|---|---|---|
| Customer diversity table | | | ⬜ | |
| Association type evidence (Customer 1) | | | ⬜ | |
| Association type evidence (Customer 2) | | | ⬜ | |
| Association type evidence (Customer 3) | | | ⬜ | |

---

## Common Gaps

| Gap | Remediation |
|---|---|
| Only 1–2 customers meet the association criteria | Urgently establish DPOR or PAL links with additional customers where you deliver Azure Local / Arc services |
| ACR concentrated in one customer | Cannot be resolved short-term; plan to diversify customer base for the next ACR window |
| Customer association records not exportable | Take screenshots from Partner Center's customer association views; annotate with customer IDs |
| Revenue from ineligible services | Review the full eligible service list and ensure customer hybrid workloads are correctly categorised |
| Customer is on Azure Stack HCI legacy SKU | Still counts — Azure Local rebrand preserves existing billing meters |

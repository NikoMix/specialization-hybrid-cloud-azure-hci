#!/usr/bin/env bash
# create-issues.sh
# Creates all audit engagement issues for the Hybrid Cloud Infrastructure with
# Microsoft Azure Local Advanced Specialization. Skips any issue whose title
# already exists (open or closed) to avoid duplicates across re-runs.
#
# Environment variables expected:
#   GH_TOKEN     - GitHub token with issues:write permission
#   CYCLE_LABEL  - e.g. "audit-2026"
#   MILESTONE    - milestone title (e.g. "Audit 2026") — passed by title for safety
#   REPO         - owner/repo
#   SITE_URL     - optional; base URL of the published guide. Defaults to the
#                  GitHub Pages project URL derived from REPO.

set -euo pipefail

# Each issue links to its control page on the published Hugo site rather than to
# a source file, so the link works from the GitHub issue UI. GitHub Pages serves
# project sites from a lower-cased owner host, so normalise the derived URL.
SITE_URL="${SITE_URL:-https://$(printf '%s' "${REPO%%/*}" | tr '[:upper:]' '[:lower:]').github.io/${REPO##*/}}"
SITE_URL="${SITE_URL%/}"

# ─── helpers ──────────────────────────────────────────────────────────────────

create_issue() {
  local title="$1"
  local labels="$2"
  local body="$3"

  # Dedup check: list all issues with this cycle's label and compare titles locally.
  # Avoids the Search API (which can return stale or filtered results on private repos).
  local existing
  existing=$(gh issue list \
    --repo "$REPO" \
    --state all \
    --label "$CYCLE_LABEL" \
    --limit 200 \
    --json title \
    --jq "[.[] | select(.title == \"$title\")] | length")

  if [ "${existing:-0}" -gt 0 ]; then
    echo "⏭  Skipping (exists): $title"
    return
  fi

  gh issue create \
    --repo "$REPO" \
    --title "$title" \
    --label "$labels" \
    --milestone "$MILESTONE" \
    --body "$body"

  echo "✅ Created: $title"
}

# ─── Pre-Qualification Gate ───────────────────────────────────────────────────

create_issue \
  "🎯 Pre-Qualification Gate" \
  "pre-qualification,$CYCLE_LABEL" \
  "## Pre-Qualification Gate

Confirm all four pre-qualification requirements are met **before** requesting the audit from Partner Center.
Once every checkbox is ticked, close this issue and proceed to request the audit.

📖 [Full requirements guide]($SITE_URL/docs/requirements/)

> ⚠️ **TODO: verify against spec PDF** — ACR threshold (USD), measurement window, exact certification list, and minimum unique individual count must be confirmed against the current Microsoft-issued *Hybrid Cloud Infrastructure with Microsoft Azure Local Advanced Specialization* requirements document.

---

### 1 – Solutions Partner Designation

- [ ] Active **Solutions Partner for Infrastructure (Azure)** confirmed in Partner Center
- [ ] Screenshot of active designation exported from Partner Center → Overview → Membership

---

### 2a – ACR Performance (Azure Local / Arc / Hybrid Resiliency)

Eligible services include: Azure Local instances, Azure Stack HCI billing meters, Arc-enabled servers, Arc-enabled Kubernetes (AKS hybrid / AKS enabled by Arc), Arc-enabled data services, Azure Backup, Azure Site Recovery, Azure Monitor, Azure Update Manager, Microsoft Defender for Cloud.

- [ ] ACR for eligible categories confirmed ≥ spec threshold in Partner Center → Insights → Azure Revenue
- [ ] ACR figure verified with PDM (data may lag 2–4 weeks)
- [ ] Partner Center ACR export saved for evidence

### 2b – Customer Diversity

- [ ] ≥ 3 unique customers contributing eligible ACR confirmed *(verify exact count against spec)*
- [ ] All contributing customers linked via DPOR, PAL, or CSP association

---

### 3 – Certifications

- [ ] **Windows Server Hybrid Administrator Associate (AZ-800 + AZ-801)** held by ≥ 1 individual — transcript link collected
- [ ] **Azure Administrator Associate (AZ-104)** held by ≥ 1 individual — transcript link collected
- [ ] **Azure Solutions Architect Expert (AZ-305)** held by ≥ 1 individual — transcript link collected
- [ ] Total certified individuals meets spec minimum *(verify exact count against spec)*
- [ ] All certifications are currently **active** (not expired)
- [ ] Certification mapping table completed (see issue B.3.1)

---

### 4 – Audit Request

- [ ] All issues in this milestone are closed ✅
- [ ] Evidence package structured and indexed (see issue B.4.1)
- [ ] Audit requested via **Partner Center → Benefits → Advanced Specializations**
- [ ] Kickoff call with auditor scheduled

---

**Close this issue** once the audit has been successfully passed. The scheduled workflow will automatically reopen a fresh set of issues 9 months later to prepare for the next annual audit cycle."

# ─── Module A ─────────────────────────────────────────────────────────────────

create_issue \
  "A.1.1 – Organisational Data" \
  "module-a,$CYCLE_LABEL" \
  "## A.1.1 – Organisational Data

Provide evidence of your organisation's legal identity and reporting structure.

📖 [Evidence guide]($SITE_URL/docs/module-a/1-1-organizational-data/)

---

### Evidence Checklist

- [ ] **Certificate of Incorporation** (or equivalent legal registration) obtained as PDF
- [ ] Company registration number is visible in the document
- [ ] Document sourced from the official national business registry (Companies House, KvK, Handelsregister, etc.)
- [ ] **Organisational chart** prepared showing all reporting lines
- [ ] Org chart includes leadership, technical delivery, and account management layers
- [ ] **Key personnel list** prepared: Name | Title | Responsibility | Certifications
- [ ] Registered address in documents matches official company records
- [ ] All documents are current (within last 3 years or confirmed as active)

### Submission Readiness

- [ ] Files named per convention: \`A1.1_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module A / A1.1\`
- [ ] Internal review completed by Delivery Lead

---
**Close this issue** when all evidence is collected, named, and ready for auditor submission."

create_issue \
  "A.1.2 – Financial Documentation" \
  "module-a,$CYCLE_LABEL" \
  "## A.1.2 – Financial Documentation

Provide evidence of financial viability and adequate professional insurance.

📖 [Evidence guide]($SITE_URL/docs/module-a/1-2-financial-documentation/)

---

### Evidence Checklist

- [ ] **Financial statements** (most recent year) obtained — audited, reviewed, or filed accounts
- [ ] Financial statements signed by an external auditor, accountant, or company director
- [ ] Revenue and profit/loss lines are visible (may redact other sensitive figures)
- [ ] **Professional Indemnity / Errors & Omissions insurance certificate** obtained
- [ ] Insurance certificate names the correct **legal entity** (matches A.1.1)
- [ ] Insurance coverage amount is visible
- [ ] Insurance policy period is **currently active**
- [ ] **Public Liability insurance certificate** obtained (if applicable)

### Submission Readiness

- [ ] Files named per convention: \`A1.2_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module A / A1.2\`
- [ ] Insurance expiry date noted and renewal reminder set

---
**Close this issue** when all evidence is collected, named, and ready for auditor submission."

create_issue \
  "A.2.1 – Service Delivery Methodology" \
  "module-a,$CYCLE_LABEL" \
  "## A.2.1 – Service Delivery Methodology

Demonstrate a documented, repeatable methodology used for service delivery.

📖 [Evidence guide]($SITE_URL/docs/module-a/2-1-service-delivery-methodology/)

---

### Evidence Checklist

- [ ] **Delivery methodology document** (playbook, handbook, or SOP) exists and is version-controlled
- [ ] Methodology covers all phases: Discovery → Design → Build → Test → Deploy → Handover
- [ ] Each phase lists key activities, artefacts produced, and responsible roles
- [ ] Quality gates between phases are defined
- [ ] Tools used (Azure DevOps, Jira, GitHub Projects, etc.) are referenced
- [ ] Document has a version number, last-reviewed date, and named owner
- [ ] **SOW / Project Charter template** prepared
- [ ] **Risk register / issue log template** prepared
- [ ] **RACI template** prepared
- [ ] **Project kickoff artefact** from a real engagement (anonymised) available
- [ ] **Project closure / handover document** from a real engagement (anonymised) available
- [ ] At least 2 different customer engagement artefacts included

### Submission Readiness

- [ ] Customer names anonymised in all real-engagement documents
- [ ] Files named per convention: \`A2.1_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module A / A2.1\`

---
**Close this issue** when all evidence is collected, named, and ready for auditor submission."

create_issue \
  "A.2.2 – Quality Management" \
  "module-a,$CYCLE_LABEL" \
  "## A.2.2 – Quality Management

Provide evidence of a quality management system, CSAT process, and escalation procedure.

📖 [Evidence guide]($SITE_URL/docs/module-a/2-2-quality-management/)

---

### Evidence Checklist

**Quality Management Policy**
- [ ] Quality policy document exists and is version-controlled
- [ ] Policy defines measurable quality objectives (e.g. ≥ 85% CSAT)
- [ ] Policy includes a management commitment statement
- [ ] Roles responsible for quality are named
- [ ] Policy has been reviewed within the last 12 months
- [ ] ISO 9001 certificate held *(if yes, this satisfies the entire control — attach certificate)*

**Customer Satisfaction (CSAT) Process**
- [ ] CSAT process document describes when, how, and to whom surveys are sent
- [ ] CSAT survey template or screenshot available
- [ ] Process describes how low scores trigger escalation or account review
- [ ] CSAT results from the last 12 months available (summary: average score, response count, trend)

**Escalation Procedure**
- [ ] Escalation procedure document defines trigger conditions, owners, and SLAs per level
- [ ] Escalation procedure is referenced in or linked from the quality policy
- [ ] At least one anonymised example of the escalation procedure being followed

### Submission Readiness

- [ ] Files named per convention: \`A2.2_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module A / A2.2\`

---
**Close this issue** when all evidence is collected, named, and ready for auditor submission."

create_issue \
  "A.3.1 – Customer Satisfaction Outcomes" \
  "module-a,$CYCLE_LABEL" \
  "## A.3.1 – Customer Satisfaction Outcomes

Provide actual CSAT/NPS outcome data and customer references demonstrating delivery quality.

📖 [Evidence guide]($SITE_URL/docs/module-a/3-1-customer-satisfaction/)

---

### Evidence Checklist

**CSAT / NPS Data**
- [ ] CSAT or NPS results from the **last 12 months** available
- [ ] Summary shows: average score, number of responses, trend over time
- [ ] Data sourced from a verifiable tool (Microsoft Forms, SurveyMonkey, CRM export, etc.)
- [ ] At least one low-score case documented with action taken

**Customer References**
- [ ] Reference summary prepared for **Customer 1** (industry, engagement, outcome, CSAT score)
- [ ] Reference summary prepared for **Customer 2** (industry, engagement, outcome, CSAT score)
- [ ] References cover at least 2 different industries or workload types
- [ ] Customer contact available for auditor verification (confirm with each customer)

**Testimonials**
- [ ] Written testimonial obtained from **Customer 1** (email or letterhead)
- [ ] Written testimonial obtained from **Customer 2** (email or letterhead)
- [ ] Each testimonial references the type of service delivered and a date

### Submission Readiness

- [ ] Customer names anonymised where required
- [ ] Files named per convention: \`A3.1_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module A / A3.1\`

---
**Close this issue** when all evidence is collected, named, and ready for auditor submission."

create_issue \
  "A.3.2 – Complaint Handling" \
  "module-a,$CYCLE_LABEL" \
  "## A.3.2 – Complaint Handling

Demonstrate a formal complaint handling process with a log and at least one resolved case.

📖 [Evidence guide]($SITE_URL/docs/module-a/3-2-complaint-handling/)

---

### Evidence Checklist

**Complaint Handling Procedure**
- [ ] Complaint handling procedure document exists and is version-controlled
- [ ] Procedure defines what qualifies as a complaint vs. a service request
- [ ] Procedure specifies how complaints are raised (contact details, form, email)
- [ ] Acknowledgement SLA defined (e.g. within 1 business day)
- [ ] Resolution SLA defined per severity level
- [ ] Escalation path is documented (aligned with A.2.2 escalation procedure)
- [ ] Recording requirements defined (where and by whom complaints are logged)
- [ ] Root cause and corrective action steps included

**Complaint Register**
- [ ] Complaint register exists (spreadsheet or system export)
- [ ] Register includes: ID, date, description, severity, owner, status, resolution date
- [ ] Register has been updated within the last 6 months

**Case Evidence**
- [ ] At least one complete case documented: receipt → investigation → resolution
- [ ] Root cause analysis completed for at least one case
- [ ] Corrective action documented and implemented

### Submission Readiness

- [ ] Customer names anonymised in all logs and case documents
- [ ] Files named per convention: \`A3.2_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module A / A3.2\`

---
**Close this issue** when all evidence is collected, named, and ready for auditor submission."

create_issue \
  "A.3.3 – Security & Privacy" \
  "module-a,$CYCLE_LABEL" \
  "## A.3.3 – Security & Privacy

Provide evidence of information security and data protection policies in active use.

📖 [Evidence guide]($SITE_URL/docs/module-a/3-3-security-privacy/)

---

### Evidence Checklist

**Information Security Policy**
- [ ] Information security policy document exists, references a recognised framework (NIST, CIS, ISO 27001)
- [ ] Policy covers: access control, authentication standards, device management, data classification, incident response, third-party risk
- [ ] Policy reviewed within the last 12 months (version number and review date visible)
- [ ] Policy approved/signed by a director or CISO
- [ ] ISO 27001 or SOC 2 Type II certificate held *(if yes, attaches certificate — satisfies this control)*

**Data Protection / Privacy Policy**
- [ ] Data protection policy document exists
- [ ] Policy covers: lawful basis, retention/deletion schedules, SAR process, cross-border transfer controls
- [ ] Organisation registered with the relevant data protection authority (e.g. ICO in UK)
- [ ] **Data Processing Agreement (DPA) template** used with customers is available

**Data Breach Response**
- [ ] Data breach response procedure documented
- [ ] Procedure covers: detection, containment, supervisory authority notification (72h for GDPR), data subject notification, post-incident review

**Staff Awareness**
- [ ] Staff security awareness training records available (last 12 months)
- [ ] Training records show name, date completed, and training title
- [ ] All staff (or a defined in-scope group) covered

### Submission Readiness

- [ ] Files named per convention: \`A3.3_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module A / A3.3\`

---
**Close this issue** when all evidence is collected, named, and ready for auditor submission."

# ─── Module B ─────────────────────────────────────────────────────────────────

create_issue \
  "B.1.1 – Azure Local Implementation Capability" \
  "module-b,$CYCLE_LABEL" \
  "## B.1.1 – Azure Local Implementation Capability

Demonstrate practical experience deploying and operating Microsoft Azure Local clusters (and Arc-connected hybrid services) for real customers on validated hardware.

📖 [Evidence guide]($SITE_URL/docs/module-b/1-1-azure-local-implementation/)

---

### Evidence Checklist

**Case Studies (minimum 2)**
- [ ] Case study 1 prepared — includes: industry, challenge, validated hardware SKU, Azure services used, outcome, your team's role
- [ ] Case study 1 explicitly names Azure Local (or Azure Stack HCI for legacy) and the Arc services in scope
- [ ] Case study 2 prepared — covers a different industry or workload type
- [ ] Case study 2 explicitly names Azure Local and the Arc services in scope
- [ ] Both case studies include a measurable customer outcome (consolidation ratio, RPO/RTO, footprint reduction, etc.)

**Architecture Diagrams (minimum 2)**
- [ ] Architecture diagram 1 shows: node count, network topology (storage/management/compute), Arc enrolment, Azure services connected
- [ ] Architecture diagram 1 shows: identity & security components (Entra ID Hybrid, AD, BitLocker, Defender)
- [ ] Architecture diagram 2 from a different engagement
- [ ] Diagrams are in PDF, Visio, or draw.io format

**Bill of Materials (BoM)**
- [ ] BoM provided for at least one delivered cluster
- [ ] Hardware SKU is on the Azure Local validated catalogue (Dell AX, HPE for Azure Local, Lenovo ThinkAgile MX, DataON, etc.)
- [ ] BoM lists CPU / memory / cache + capacity disks / network adapters per node

**Deployment Runbook / As-built**
- [ ] Runbook or as-built document from a real engagement available (anonymised)
- [ ] Document covers cluster deployment steps, Network ATC intent, S2D volume layout, Arc enrolment, monitoring & backup wiring

**Service Capability Statement**
- [ ] One-page capability statement listing Azure Local / Arc capabilities your team delivers
- [ ] Statement includes number of completed clusters per validated hardware vendor
- [ ] Statement references key team members and their certifications

### Submission Readiness

- [ ] Customer names anonymised across all documents
- [ ] Files named per convention: \`B1.1_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module B / B1.1\`

---
**Close this issue** when all evidence is collected, named, and ready for auditor submission."

create_issue \
  "B.2.1 – ACR Performance" \
  "module-b,$CYCLE_LABEL" \
  "## B.2.1 – ACR Performance

Demonstrate the spec-required Azure Consumed Revenue from eligible Azure Local / Arc / hybrid resiliency services across the measurement window.

📖 [Evidence guide]($SITE_URL/docs/module-b/2-1-acr-performance/)

> ⚠️ **TODO: verify against spec PDF** — exact USD threshold, measurement window length, and per-category split (if any) must be confirmed against the current Microsoft-issued spec document.

---

### Eligible Service Categories

- **Azure Local / Azure Stack HCI:** Azure Local instances, legacy HCI billing meters
- **Azure Arc:** Arc-enabled servers, Arc-enabled Kubernetes (AKS hybrid / AKS enabled by Arc), Arc-enabled data services
- **Hybrid resiliency:** Azure Backup, Azure Site Recovery
- **Hybrid observability & ops:** Azure Monitor, Log Analytics, Azure Update Manager, Microsoft Defender for Cloud

---

### Checklist

- [ ] Partner Center ACR export obtained (full measurement window)
- [ ] Eligible-category total confirmed: **\$ ______** (≥ spec threshold ✅ / below threshold ❌)
- [ ] Data confirmed with PDM (lag adjusted)
- [ ] All contributing subscriptions linked via DPOR, PAL, or CSP
- [ ] Partner Center ACR export annotated to show category breakdowns
- [ ] PDF/Excel export saved with date in filename
- [ ] Association type (DPOR/PAL/CSP) screenshots or exports included

### Submission Readiness

- [ ] Files named per convention: \`B2.1_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module B / B2.1\`

---
**Close this issue** when the eligible categories meet the threshold and evidence is ready for submission."

create_issue \
  "B.2.2 – Customer Diversity (≥ 3 Unique Customers)" \
  "module-b,$CYCLE_LABEL" \
  "## B.2.2 – Customer Diversity

Demonstrate the spec-required number of unique customers contributing eligible ACR across Azure Local / Arc / hybrid resiliency services.

📖 [Evidence guide]($SITE_URL/docs/module-b/2-2-customer-diversity/)

> ⚠️ **TODO: verify against spec PDF** — confirm the exact minimum unique customer count (3 is typical) against the current spec document.

---

### Customer Mapping (complete one block per customer)

**Customer 1**
- [ ] Customer 1 identified in Partner Center ACR data
- [ ] Association type confirmed: DPOR / PAL / CSP
- [ ] Eligible service(s) contributing: ______
- [ ] ACR contribution (measurement window): \$ ______

**Customer 2**
- [ ] Customer 2 identified in Partner Center ACR data
- [ ] Association type confirmed: DPOR / PAL / CSP
- [ ] Eligible service(s) contributing: ______
- [ ] ACR contribution (measurement window): \$ ______

**Customer 3**
- [ ] Customer 3 identified in Partner Center ACR data
- [ ] Association type confirmed: DPOR / PAL / CSP
- [ ] Eligible service(s) contributing: ______
- [ ] ACR contribution (measurement window): \$ ______

*(Add Customer 4, 5... if applicable / required by spec)*

### Evidence Package

- [ ] Customer diversity mapping table prepared (anonymised: Customer A, B, C…)
- [ ] Association type screenshots/exports included for each customer
- [ ] Partner Center 'Revenue by Customer' view export saved

### Submission Readiness

- [ ] Customer names anonymised in all submitted documents
- [ ] Files named per convention: \`B2.2_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module B / B2.2\`

---
**Close this issue** when the spec-required number of unique customers is confirmed and evidence is ready for submission."

create_issue \
  "B.3.1 – Certifications" \
  "module-b,$CYCLE_LABEL" \
  "## B.3.1 – Certifications

The spec-required individuals must hold the required Azure infrastructure certifications.

📖 [Evidence guide]($SITE_URL/docs/module-b/3-1-certifications/)

> ⚠️ **TODO: verify against spec PDF** — confirm the exact required certification list, the minimum number of unique individuals, and whether AZ-800 + AZ-801 by the same person count as one or two holders.

---

### Required Certifications — Holder Confirmation

**Windows Server Hybrid Administrator Associate (AZ-800 + AZ-801)** _(minimum 1 holder)_
- [ ] Holder identified: __________________
- [ ] AZ-800 currently active (not expired) — transcript collected
- [ ] AZ-801 currently active (not expired) — transcript collected
- [ ] Holder is an employee (not a contractor) — or contractor status confirmed acceptable

**AZ-104 – Azure Administrator Associate** _(minimum 1 holder — verify against spec)_
- [ ] Holder identified: __________________
- [ ] Certification currently active (not expired)
- [ ] Microsoft Learn transcript link or PDF export collected

**AZ-305 – Azure Solutions Architect Expert** _(minimum 1 holder — verify against spec)_
- [ ] Holder identified: __________________
- [ ] Certification currently active (not expired)
- [ ] Microsoft Learn transcript link or PDF export collected

**Additional individuals (per spec minimum count)**
- [ ] Additional individual(s) identified to meet spec minimum: __________________
- [ ] Certification(s) held: __________________
- [ ] Certifications currently active
- [ ] Transcripts collected

### Evidence Package

- [ ] Certification mapping table completed: Name | Role | Cert | Exam Code | Issue Date | Expiry | Transcript Link
- [ ] All individuals' Learn profiles set to **public** or PDF transcripts exported
- [ ] Expiry dates tracked — renewal reminders set for any cert expiring within 6 months

### Submission Readiness

- [ ] Files named per convention: \`B3.1_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module B / B3.1\`

---
**Close this issue** when all required individuals are confirmed, certs are active, and transcripts are collected."

create_issue \
  "B.4.1 – Audit Readiness & Evidence Package" \
  "module-b,$CYCLE_LABEL" \
  "## B.4.1 – Audit Readiness

Structured, indexed evidence package ready for auditor submission.

📖 [Evidence guide]($SITE_URL/docs/module-b/4-1-audit-readiness/)

---

### Pre-Submission: All Controls Complete?

- [ ] A.1.1 – Organisational Data ✅
- [ ] A.1.2 – Financial Documentation ✅
- [ ] A.2.1 – Service Delivery Methodology ✅
- [ ] A.2.2 – Quality Management ✅
- [ ] A.3.1 – Customer Satisfaction Outcomes ✅
- [ ] A.3.2 – Complaint Handling ✅
- [ ] A.3.3 – Security & Privacy ✅
- [ ] B.1.1 – Azure Local Implementation Capability ✅
- [ ] B.2.1 – ACR Performance ✅
- [ ] B.2.2 – Customer Diversity ✅
- [ ] B.3.1 – Certifications ✅
- [ ] B.4.2 – Partner Onboarding Assets ✅

### Evidence Package Structure

- [ ] Folder structure created: one sub-folder per control (e.g. \`Module A / A1.1\`)
- [ ] All files named per convention: \`[ControlRef]_[DocumentType]_v[N].pdf\`
- [ ] **Evidence Index spreadsheet** created mapping each control → files → version → date
- [ ] No broken links, missing pages, or placeholder text in any document
- [ ] Customer names anonymised across all documents

### Internal Review

- [ ] Internal evidence review completed with Delivery Lead + Technical Lead
- [ ] Any gaps identified in review have been resolved
- [ ] Evidence package signed off by engagement lead

### Submission

- [ ] Auditor submission channel confirmed (SharePoint / email / portal)
- [ ] Evidence package submitted to auditor
- [ ] Auditor receipt confirmed in writing
- [ ] Kickoff / review call with auditor completed

### Remediation (complete if applicable)

- [ ] Remediation report received from auditor
- [ ] Each finding addressed and re-submitted within 30 days
- [ ] Auditor confirmed remediation accepted

---
**Close this issue** when the audit has been **passed** and the specialization badge is confirmed in Partner Center."

create_issue \
  "B.4.2 – Partner Onboarding Assets" \
  "module-b,$CYCLE_LABEL" \
  "## B.4.2 – Partner Onboarding Assets

Provide structured customer onboarding materials and delivery templates for Azure Local engagements.

📖 [Evidence guide]($SITE_URL/docs/module-b/4-2-partner-onboarding/)

---

### Customer Onboarding Pack

- [ ] Onboarding pack exists as a branded document (PDF or PowerPoint)
- [ ] Pack includes: introduction to your organisation and key contacts
- [ ] Pack includes: engagement overview (scope, timeline, milestones, deliverables — site survey → BoM → deployment → validation → handover)
- [ ] Pack includes: communication cadence (meeting frequency, reporting format, tools)
- [ ] Pack includes: Azure environment standards (naming conventions, tagging, governance, landing zone alignment)
- [ ] Pack includes: Azure Local environment standards (cluster naming, RBAC, monitoring baseline, patching cadence)
- [ ] Pack includes: support model post go-live (incident response, SLAs, OEM hardware escalation)
- [ ] Pack has been used in at least one real customer engagement

### Delivery Templates (minimum 2 from different phases)

- [ ] Template 1 prepared — phase: ______ — type: ______
- [ ] Template 2 prepared — phase: ______ — type: ______
- [ ] Templates are reusable (not customer-specific — or generalised from a real engagement)

_Suggested templates: site survey, Azure Local sizing workbook, HLD, cluster validation script set, go-live checklist, hypercare plan, closure report_

### Knowledge Transfer Plan

- [ ] KT plan template exists
- [ ] Plan covers: scope of knowledge to transfer, format (docs/workshops/recordings), recipients, timeline, validation method (e.g. witnessed patch cycle, witnessed DR test)
- [ ] KT plan integrated into delivery methodology (A.2.1)

### Customer Operational Runbook for an Azure Local Cluster (anonymised)

- [ ] Operational runbook exists for at least one delivered Azure Local cluster
- [ ] Runbook covers: architecture overview, day-to-day operations, monitoring & alerting, patching (Azure Update Manager + OEM firmware), backup & DR, common issues, escalation contacts, cost management
- [ ] Customer name anonymised

### Submission Readiness

- [ ] Files named per convention: \`B4.2_[DocumentType]_v[N].pdf\`
- [ ] Documents added to evidence package folder \`Module B / B4.2\`

---
**Close this issue** when all onboarding assets are collected, named, and ready for auditor submission."

echo ""
echo "🎉 Issue creation complete."

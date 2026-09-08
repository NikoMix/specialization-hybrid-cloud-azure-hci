"""Generate downloadable workfiles for the Azure Local specialization engagement playbook.

Outputs land under `static/templates/{engagement,deliverables,audit}/`.
Idempotent — safe to re-run.
"""

from __future__ import annotations

import os
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

from pptx import Presentation
from pptx.util import Inches as PInches, Pt as PPt
from pptx.dml.color import RGBColor as PRGBColor

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter


ROOT = Path(__file__).resolve().parents[1]
TPL = ROOT / "static" / "templates"
NEUTRAL_BLUE = "1F4E79"
LIGHT_BLUE = "D9E2F3"
WHITE = "FFFFFF"


def _word_cover(doc, title, subtitle):
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("\n\n\n")
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(28)
    run.font.color.rgb = RGBColor.from_string(NEUTRAL_BLUE)
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p2.add_run(subtitle)
    run.italic = True
    run.font.size = Pt(14)
    doc.add_paragraph()
    pmeta = doc.add_paragraph()
    pmeta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pmeta.add_run(
        "Customer: ______________________     Engagement: ______________________     "
        "Version: 0.1     Date: __________"
    ).font.size = Pt(11)
    doc.add_page_break()


def _word_toc(doc, sections):
    h = doc.add_heading("Table of Contents", level=1)
    if h.runs:
        h.runs[0].font.color.rgb = RGBColor.from_string(NEUTRAL_BLUE)
    for i, s in enumerate(sections, start=1):
        p = doc.add_paragraph(f"{i}. {s}")
        p.paragraph_format.left_indent = Inches(0.25)
    note = doc.add_paragraph()
    r = note.add_run(
        "(Right-click in Word -> Update Field to regenerate live TOC once headings are finalised.)"
    )
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    doc.add_page_break()


def _word_section(doc, heading, prompt):
    h = doc.add_heading(heading, level=1)
    if h.runs:
        h.runs[0].font.color.rgb = RGBColor.from_string(NEUTRAL_BLUE)
    p = doc.add_paragraph()
    r = p.add_run(prompt)
    r.italic = True
    r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    doc.add_paragraph()


def _word_doc(path, title, subtitle, sections):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    _word_cover(doc, title, subtitle)
    _word_toc(doc, [s[0] for s in sections])
    for heading, prompt in sections:
        _word_section(doc, heading, prompt)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)


def _pptx_set_bg(slide, color_hex):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = PRGBColor.from_string(color_hex)


def _style_title(shape, size=28):
    if not shape.has_text_frame:
        return
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.bold = True
            r.font.size = PPt(size)
            r.font.color.rgb = PRGBColor.from_string(NEUTRAL_BLUE)


def _style_body(shape):
    if not shape.has_text_frame:
        return
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = PPt(18)


def _pptx(path, title, subtitle, agenda, sections, next_steps):
    prs = Presentation()
    prs.slide_width = PInches(13.33)
    prs.slide_height = PInches(7.5)

    # Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    _pptx_set_bg(slide, WHITE)
    slide.shapes.title.text = title
    if len(slide.placeholders) > 1:
        slide.placeholders[1].text = subtitle
    _style_title(slide.shapes.title, size=36)
    for ph in slide.placeholders:
        if ph != slide.shapes.title:
            _style_body(ph)

    def _add(title_text, bullets):
        s = prs.slides.add_slide(prs.slide_layouts[1])
        _pptx_set_bg(s, WHITE)
        s.shapes.title.text = title_text
        body = s.placeholders[1].text_frame
        body.text = bullets[0] if bullets else ""
        for b in bullets[1:]:
            body.add_paragraph().text = b
        _style_title(s.shapes.title, size=28)
        for ph in s.placeholders:
            if ph != s.shapes.title:
                _style_body(ph)

    _add("Agenda", agenda)
    for sec_title, bullets in sections:
        _add(sec_title, bullets)
    _add("Next steps", next_steps)

    path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(path)


HEADER_FILL = PatternFill("solid", fgColor=NEUTRAL_BLUE)
HEADER_FONT = Font(bold=True, color=WHITE, name="Calibri", size=11)
ALT_FILL = PatternFill("solid", fgColor=LIGHT_BLUE)
THIN = Side(border_style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
STATUS_LIST = '"Not started,In progress,Blocked,Complete,N/A"'


def _xlsx_header(ws, headers):
    for col, h in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(col)].width = max(18, min(40, len(h) + 6))
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 22


def _xlsx_status(ws, col_letter, rows=200):
    dv = DataValidation(type="list", formula1=STATUS_LIST, allow_blank=True)
    dv.add(f"{col_letter}2:{col_letter}{rows}")
    ws.add_data_validation(dv)


def _xlsx_fill(ws, rows):
    for r_idx, row in enumerate(rows, start=2):
        for c_idx, val in enumerate(row, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORDER
            if r_idx % 2 == 0:
                cell.fill = ALT_FILL


# ── engagement ────────────────────────────────────────────────────────────

def gen_offering_one_pager():
    path = TPL / "engagement" / "offering-one-pager.pptx"
    _pptx(
        path,
        "Azure Local Managed Platform",
        "First-cluster landing zone - offering one-pager",
        ["Why Azure Local", "In scope", "Out of scope", "Outcomes",
         "Indicative commercials", "Next steps"],
        [
            ("Why Azure Local", [
                "Hybrid by design - Azure operations on customer-controlled hardware",
                "Validated hardware catalog removes integration risk",
                "Arc-native - single pane across cloud + on-prem + edge",
            ]),
            ("In scope", [
                "Discovery workshop (1 day)",
                "HLD + LLD using repo templates",
                "BoM + vendor coordination",
                "First cluster build (2-16 nodes)",
                "Arc enrolment + Monitor + Defender + Update Manager + Backup",
                "4-week hypercare and KT",
            ]),
            ("Out of scope", [
                "Application migration / refactor",
                "AKS on Azure Local (add-on module)",
                "Multi-site stretch / DR (add-on module)",
                "Long-term managed-service operations",
            ]),
            ("Outcomes", [
                "Healthy Arc-enrolled cluster",
                "Monitoring + backup + DR tested",
                "Ops runbook signed off",
                "Audit-grade evidence pack added to repo",
            ]),
            ("Indicative commercials", [
                "Edge / branch (2-node) - 4-6 weeks",
                "Standard datacentre (4-8 node) - 6-10 weeks",
                "Aggregation / sovereign (8-16 node + stretch) - 10-14 weeks",
                "Replace bands with local rate card before sharing externally",
            ]),
        ],
        ["Send qualification questionnaire", "Book 1-day discovery workshop",
         "Confirm exec sponsor + steering committee"],
    )
    return path


def gen_qualification_questionnaire():
    path = TPL / "engagement" / "qualification-questionnaire.docx"
    _word_doc(path, "Customer Qualification Questionnaire",
              "Azure Local hybrid-infrastructure engagement", [
        ("1. Strategic fit", "Capture the business driver, exec sponsor, and 12-month success picture."),
        ("2. Workload fit", "List in-scope workloads with tiering, RPO/RTO, and any GPU / accelerator requirements."),
        ("3. Site topology", "Datacentre + edge / branch sites, power, cooling, on-site hands."),
        ("4. Existing Azure footprint", "Tenant + subscriptions + landing-zone maturity + current Arc usage."),
        ("5. Identity model", "Entra ID, hybrid join, on-prem AD DS, MFA + conditional access posture."),
        ("6. Connectivity per site", "Bandwidth, dual-path, ExpressRoute / VPN, proxy posture."),
        ("7. Regulatory drivers", "GDPR, NIS2, sector-specific frameworks, sovereignty requirements."),
        ("8. Operations readiness", "Who runs steady state, change-management, monitoring stack, patching cadence."),
        ("9. Commercial and procurement", "Preferred validated vendor, procurement vehicle, budget approval status."),
        ("10. Go / no-go scoring", "Score each dimension red / amber / green. Two reds = no-go."),
    ])
    return path


def gen_discovery_deck():
    path = TPL / "engagement" / "discovery-workshop-deck.pptx"
    _pptx(path, "Azure Local Discovery Workshop",
          "1-day workshop - outcomes, current state, target state, risks",
          ["Outcomes alignment", "Current state", "Target pattern",
           "Workload placement", "Validated hardware", "Arc + observability",
           "DR + backup", "Risks + decisions"],
          [
              ("Outcomes alignment", [
                  "Confirm business outcomes and 12-month success picture",
                  "Confirm decision rights and steering committee",
              ]),
              ("Current state", ["Capture topology, hypervisor, host count, pain points"]),
              ("Target pattern", ["Single-site / branch / stretch / edge / AKS-on-Local"]),
              ("Workload placement", ["Tiered workload table - VM / SQL / AKS / GPU"]),
              ("Validated hardware", ["Long-list of two vendor options from Azure Local catalog"]),
              ("Arc + observability", ["Arc scope, Azure Monitor / Defender / Sentinel plan"]),
              ("DR + backup", ["RPO / RTO per workload tier, Backup + ASR strategy"]),
              ("Risks + decisions", ["Decision log + draft HLD scope statement"]),
          ],
          ["Discovery report within 5 business days", "HLD kickoff scheduled"])
    return path


def gen_discovery_workbook():
    path = TPL / "engagement" / "discovery-workshop-workbook.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Current state"
    _xlsx_header(ws, ["#", "Site", "Hypervisor", "Hosts", "VM count", "Notes"])
    _xlsx_fill(ws, [[i, "", "", "", "", ""] for i in range(1, 11)])

    ws2 = wb.create_sheet("Target state")
    _xlsx_header(ws2, ["#", "Site", "Pattern", "Nodes", "Vendor", "Notes"])
    _xlsx_fill(ws2, [[i, "", "", "", "", ""] for i in range(1, 11)])

    ws3 = wb.create_sheet("Workloads")
    _xlsx_header(ws3, ["#", "Workload", "Tier", "RPO", "RTO", "Target placement", "Status"])
    _xlsx_fill(ws3, [[i, "", "", "", "", "", "Not started"] for i in range(1, 21)])
    _xlsx_status(ws3, "G")

    ws4 = wb.create_sheet("Risks")
    _xlsx_header(ws4, ["#", "Risk", "Owner", "Mitigation", "Status"])
    _xlsx_fill(ws4, [[i, "", "", "", "Not started"] for i in range(1, 16)])
    _xlsx_status(ws4, "E")

    ws5 = wb.create_sheet("Decision log")
    _xlsx_header(ws5, ["#", "Decision", "Decided by", "Date", "Rationale"])
    _xlsx_fill(ws5, [[i, "", "", "", ""] for i in range(1, 16)])

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path


def gen_waf_assessment():
    path = TPL / "engagement" / "waf-assessment.xlsx"
    wb = Workbook()
    pillars = [
        ("Reliability", [
            "Cluster quorum model + witness placement",
            "Stretch cluster site-awareness + replication mode",
            "S2D resiliency tier per workload tier",
            "Validated hardware refresh cadence + spares",
            "RPO/RTO per workload tested via ASR drill",
            "Capacity headroom for N+1 node loss",
        ]),
        ("Operational Excellence", [
            "Arc-driven inventory + tagging",
            "Azure Update Manager cadence (firmware/OS/drivers)",
            "Network ATC intents vs manual config",
            "Azure Policy guest configuration baselines",
            "Runbook automation (Automation / DSC)",
            "Change management for cluster-level changes",
        ]),
        ("Security", [
            "Secured-core servers (TPM 2.0, VBS)",
            "Defender for Servers / Containers coverage",
            "Application control (WDAC) mode",
            "BitLocker on S2D + key management",
            "RBAC via Arc + Entra ID; local admin separation",
            "Microsegmentation + east-west policy",
        ]),
        ("Performance Efficiency", [
            "Cache vs capacity tier sizing",
            "Network bandwidth headroom for S2D rebuild",
            "GPU partitioning for inferencing",
        ]),
        ("Cost Optimization", [
            "Azure Local billing + Arc consumption model",
            "Hybrid Use Benefit for guest Windows Server",
            "Right-sized validated hardware vs growth model",
        ]),
    ]
    first = True
    for name, qs in pillars:
        if first:
            ws = wb.active
            ws.title = name
            first = False
        else:
            ws = wb.create_sheet(name)
        _xlsx_header(ws, ["#", "Question", "Current state", "Target state", "Risk", "Status"])
        _xlsx_fill(ws, [[i, q, "", "", "", "Not started"] for i, q in enumerate(qs, start=1)])
        _xlsx_status(ws, "F")
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path


def gen_assessment_platform_inputs():
    path = TPL / "engagement" / "assessment-platform-inputs.xlsx"
    wb = Workbook()
    platforms = [
        ("MAP", ["Host inventory CSV", "SQL inventory", "Hyper-V inventory"]),
        ("Azure Migrate", ["Appliance ID", "VM inventory + utilisation", "Dependency map"]),
        ("Arc readiness", ["Server list", "K8s clusters", "SQL estate", "Blockers"]),
        ("Azure Local Sizer", ["Workload profile", "Validated SKU candidates", "Output BoM"]),
        ("CAS Evaluator", ["Governance score", "Landing zone gaps", "Operating-model gaps"]),
    ]
    first = True
    for name, items in platforms:
        if first:
            ws = wb.active
            ws.title = name
            first = False
        else:
            ws = wb.create_sheet(name)
        _xlsx_header(ws, ["#", "Input", "Owner", "Source", "Status", "Notes"])
        _xlsx_fill(ws, [[i, q, "", "", "Not started", ""] for i, q in enumerate(items, start=1)])
        _xlsx_status(ws, "E")
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path


def gen_definition_of_done():
    path = TPL / "engagement" / "definition-of-done.docx"
    _word_doc(path, "Definition of Done",
              "Azure Local engagement exit checklist", [
        ("Cluster health", "Every node healthy in Azure portal + WAC; cluster validation clean; S2D resiliency green."),
        ("Arc enrolment", "Cluster + workloads visible in customer tenant; RBAC + tags applied per policy."),
        ("Observability", "Azure Monitor + Log Analytics + alert rules + customer dashboards delivered."),
        ("Backup and DR", "Restore test signed off; ASR drill complete; RPO/RTO documented vs HLD."),
        ("Security", "Secured-core verified; Defender + BitLocker + WDAC at expected posture."),
        ("Update management", "Azure Update Manager configured; first cycle joint; second cycle by customer."),
        ("Knowledge transfer", "Runbook delivered; KT sessions signed; top-10 day-2 ops customer-led."),
        ("Audit evidence", "Anonymised case study + diagrams + BoM + runbook added to repo evidence pack."),
        ("Innersource", "Lessons-learned issue raised; template PRs opened where applicable."),
        ("Sign-off", "Customer ops, customer security, partner delivery, partner practice - all sign and date."),
    ])
    return path


# ── deliverables ──────────────────────────────────────────────────────────

def gen_hld():
    path = TPL / "deliverables" / "hld-template.docx"
    _word_doc(path, "High-Level Design",
              "Azure Local + Arc hybrid infrastructure - HLD template", [
        ("1. Executive summary", "One page; outcomes, scope, approach, key risks, indicative timeline."),
        ("2. Business outcomes and success criteria", "Pull from discovery workbook; measurable."),
        ("3. Solution overview", "Selected pattern + Azure Architecture Center URL + customer overlay."),
        ("4. Physical architecture", "Sites, nodes, switches, BoM summary."),
        ("5. Network design", "ATC intents, VLANs, RDMA, ToR, Arc connectivity, proxy."),
        ("6. Storage design", "S2D volumes, tiers, resiliency, BitLocker."),
        ("7. Compute design", "Hyper-V, AKS on Azure Local if in scope, GPU if applicable."),
        ("8. Azure plane", "Arc, Monitor, Defender, Update Manager, Backup, Site Recovery."),
        ("9. Identity and access", "Entra ID, Arc RBAC, on-prem AD DS bindings."),
        ("10. Security posture", "Secured-core, WDAC, microsegmentation, key management."),
        ("11. DR design", "Witness, stretch, ASR, backup tiering, RPO/RTO per workload."),
        ("12. Operations model", "Who runs it, change cadence, patch cadence."),
        ("13. Risks and assumptions", "Top-10 WAF findings carried forward."),
        ("14. Roadmap", "Post go-live add-ons: AKS, Arc-SQL, stretch, GPU."),
        ("15. Appendices", "Workbooks, raw assessment exports, vendor quotes."),
    ])
    return path


def gen_lld():
    path = TPL / "deliverables" / "lld-template.docx"
    _word_doc(path, "Low-Level Design",
              "Azure Local build-engineer-grade detail", [
        ("1. Cluster identity", "Name, resource group, region, tags."),
        ("2. Per-node specification", "SKU, serial, MAC list, firmware baseline."),
        ("3. Switch and cabling map", "Port-by-port from BoM."),
        ("4. Network ATC intents", "Management / compute / storage VLAN + IP plan."),
        ("5. S2D volume layout", "Per-volume name, size, resiliency tier, workload."),
        ("6. Workload placement table", "Hyper-V VM / AKS workload allocation."),
        ("7. Arc enrolment specifics", "Service principal, proxy, tags."),
        ("8. Monitor / Defender / Update Manager config", "DCRs, workspace, policies."),
        ("9. Backup vault config", "Per-VM policy mapping."),
        ("10. Site Recovery config", "If in scope - replication, RPO target."),
        ("11. Identity bindings", "Entra ID groups -> Arc RBAC roles."),
        ("12. Security baselines", "WDAC policy file path, BitLocker key vault."),
        ("13. Post-build validation tests", "Expected output for each test."),
        ("14. Cutover plan", "Rollback triggers and decision points."),
        ("15. Appendices", "Cabling diagrams, vendor quotes, PowerShell snippets."),
    ])
    return path


def gen_runbook():
    path = TPL / "deliverables" / "runbook-template.docx"
    _word_doc(path, "Cluster Lifecycle Runbook",
              "Day 0 / 1 / 2 operations for an Azure Local cluster", [
        ("Day 0 - Pre-checks", "Firmware baseline, BIOS settings, BMC / iLO / iDRAC."),
        ("Day 0 - Network ATC", "Deploy and validate; capture intent output."),
        ("Day 0 - Cluster + S2D", "Create cluster; enable S2D; validate."),
        ("Day 0 - Register to Azure", "Azure Local registration steps."),
        ("Day 0 - Witness", "Witness type chosen + reachability test."),
        ("Day 0 - Post-build validation", "Expected output for each validation test."),
        ("Day 1 - VM onboarding", "Placement and live-migration policy."),
        ("Day 1 - AKS on Azure Local", "If in scope - workload cluster create."),
        ("Day 1 - Arc enrolment", "Guest workload Arc enrolment steps."),
        ("Day 1 - Backup policy", "Assign vault policy per VM."),
        ("Day 1 - Site Recovery", "If in scope - replication enablement."),
        ("Day 2 - Monitoring playbook", "Top 20 alerts, responder, SLA."),
        ("Day 2 - Patching cycle", "Firmware, drivers, OS, Azure Local solution updates."),
        ("Day 2 - Capacity management", "Thresholds + actions."),
        ("Day 2 - Add / remove node", "Step-by-step."),
        ("Day 2 - Volume resize / rebalance", "Step-by-step."),
        ("Day 2 - Witness failure recovery", "Step-by-step."),
        ("Day 2 - Stretch failover and failback", "Step-by-step + drill schedule."),
        ("Day 2 - Certificate rotation", "Step-by-step."),
        ("Lifecycle - Annual DR drill", "Schedule + acceptance criteria."),
        ("Lifecycle - Hardware refresh", "Trigger + procurement lead time."),
        ("Lifecycle - Decommission", "Secure data destruction + audit trail."),
    ])
    return path


def gen_kt():
    path = TPL / "deliverables" / "kt-plan-template.docx"
    _word_doc(path, "Knowledge Transfer Plan",
              "Azure Local cluster - KT sessions, audiences, proof points", [
        ("Customer ops profile", "Org chart, roles, current skills (AZ-104 / AZ-800 / AZ-801)."),
        ("Session 1 - Architecture overview", "Audience: ops + leads. 60m. Proof: drawn diagram."),
        ("Session 2 - Cluster build walk-through", "Audience: build engineers. 120m. Proof: shadowed deploy."),
        ("Session 3 - Network ATC deep-dive", "Audience: network ops. 90m. Proof: inspect ATC intent."),
        ("Session 4 - S2D operations", "Audience: storage ops. 90m. Proof: capacity report."),
        ("Session 5 - Arc enrolment + RBAC", "Audience: cloud ops. 60m. Proof: assign role."),
        ("Session 6 - Monitoring + alerts", "Audience: NOC. 90m. Proof: triage synthetic alert."),
        ("Session 7 - Patching cycle", "Audience: patch team. 60m. Proof: supervised patch."),
        ("Session 8 - Backup + restore", "Audience: backup team. 60m. Proof: restore test VM."),
        ("Session 9 - Stretch / DR drill", "Audience: DR team. 120m. Proof: failover + failback."),
        ("Session 10 - Runbook walkthrough", "Audience: all ops. 90m. Proof: signed runbook."),
        ("Sign-off log", "Per-session attendance + proof-point completion."),
    ])
    return path


def gen_hypercare():
    path = TPL / "deliverables" / "hypercare-plan-template.docx"
    _word_doc(path, "Hypercare Plan",
              "4-week structured handhold post go-live", [
        ("Week 1 - Partner leads, customer shadows", "Exit gate: first patch cycle executed jointly."),
        ("Week 2 - Joint ops + runbook handover", "Exit gate: backup restore test signed off."),
        ("Week 3 - Customer leads, partner safety net", "Exit gate: top-10 day-2 ops by customer."),
        ("Week 4 - Partner on-call only", "Exit gate: DR drill complete + DoD sign-off."),
        ("Daily stand-up (week 1-2)", "15 min - triage + blockers."),
        ("Twice-weekly stand-up (week 3-4)", "20 min - steady state."),
        ("Weekly health review", "Metrics, risks, decisions."),
        ("Final review", "Walk Definition of Done; sign-off."),
        ("Incident matrix", "Priority levels, partner vs customer ownership, on-call contacts."),
        ("Exit criteria", "All DoD items ticked; lessons learned issue raised."),
    ])
    return path


# ── audit ─────────────────────────────────────────────────────────────────

EVIDENCE_CONTROLS = [
    ("A.1.1", "Organisational Data"),
    ("A.1.2", "Financial Documentation"),
    ("A.2.1", "Service Delivery Methodology"),
    ("A.2.2", "Quality Management"),
    ("A.3.1", "Customer Satisfaction"),
    ("A.3.2", "Complaint Handling"),
    ("A.3.3", "Security and Privacy"),
    ("B.1.1", "Azure Local Implementation Capability"),
    ("B.2.1", "ACR Performance (Eligible Hybrid Services)"),
    ("B.2.2", "Customer Diversity (>=3 unique customers)"),
    ("B.3.1", "Certifications Mapping"),
    ("B.4.1", "Audit Readiness"),
    ("B.4.2", "Partner Onboarding Assets"),
]


def gen_evidence_tracker():
    path = TPL / "audit" / "evidence-tracker.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Evidence tracker"
    _xlsx_header(ws, ["Control", "Description", "Owner", "Due date", "Status", "Evidence link", "Notes"])
    rows = [[ref, desc, "", "", "Not started", "", ""] for ref, desc in EVIDENCE_CONTROLS]
    _xlsx_fill(ws, rows)
    _xlsx_status(ws, "E", rows=len(rows) + 1)

    ws2 = wb.create_sheet("Certification holders")
    _xlsx_header(ws2, ["Name", "Role", "AZ-800", "AZ-801", "AZ-104", "AZ-305", "Expiry"])
    _xlsx_fill(ws2, [["", "", "", "", "", "", ""] for _ in range(15)])

    ws3 = wb.create_sheet("ACR summary")
    _xlsx_header(ws3, ["Service category", "Representative services", "12-month ACR", "Target", "Unique customers", "Status"])
    _xlsx_fill(ws3, [
        ["Azure Local / HCI", "Azure Local instances, HCI billing meters", 0, "TODO", 0, "Not started"],
        ["Azure Arc", "Arc-enabled servers, K8s, data services", 0, "TODO", 0, "Not started"],
        ["Hybrid resiliency", "Azure Backup, Azure Site Recovery", 0, "TODO", 0, "Not started"],
        ["AKS on Azure Local", "AKS hybrid / enabled by Arc", 0, "TODO", 0, "Not started"],
    ])
    _xlsx_status(ws3, "F", rows=10)

    ws4 = wb.create_sheet("Submission log")
    _xlsx_header(ws4, ["Date", "Control", "Document", "Version", "Submitted to", "Confirmation"])

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path


def gen_pre_qual():
    path = TPL / "audit" / "pre-qual-checklist.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Pre-qualification"
    _xlsx_header(ws, ["Item", "Owner", "Status", "Evidence", "Notes"])
    items = [
        "Active Solutions Partner - Infrastructure (Azure) confirmed",
        "ACR threshold for eligible Azure Local / Arc services met",
        ">=3 unique customers contributing eligible ACR",
        "AZ-800 (Windows Server Hybrid Admin Associate) - >=1 holder",
        "AZ-801 (Configuring Windows Server Hybrid Advanced Services) - >=1 holder",
        "AZ-104 (Azure Administrator Associate) - >=1 holder",
        "AZ-305 (Azure Solutions Architect Expert) - >=1 holder",
        "Total certified individuals meets spec minimum",
        "At least one Azure Local cluster deployed on validated hardware",
        "Audit requested via Partner Center",
    ]
    rows = [[i, "", "Not started", "", ""] for i in items]
    _xlsx_fill(ws, rows)
    _xlsx_status(ws, "C", rows=len(rows) + 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path


GENERATORS = [
    gen_offering_one_pager,
    gen_qualification_questionnaire,
    gen_discovery_deck,
    gen_discovery_workbook,
    gen_waf_assessment,
    gen_assessment_platform_inputs,
    gen_definition_of_done,
    gen_hld,
    gen_lld,
    gen_runbook,
    gen_kt,
    gen_hypercare,
    gen_evidence_tracker,
    gen_pre_qual,
]


def main():
    for g in GENERATORS:
        path = g()
        rel = path.relative_to(ROOT)
        print(f"wrote {rel} ({os.path.getsize(path)} bytes)")


if __name__ == "__main__":
    main()

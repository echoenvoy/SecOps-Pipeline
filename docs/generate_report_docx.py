import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = docx.Document()

# Set standard margins (0.8 inch)
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Brand colors
PRIMARY = RGBColor(14, 116, 144)    # Deep Teal
SECONDARY = RGBColor(30, 41, 59)   # Slate Navy
DARK_TEXT = RGBColor(15, 23, 42)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

# Title
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = p_title.add_run('PROGRESS REPORT (COMPTE RENDU)')
run_title.font.name = 'Calibri'
run_title.font.size = Pt(20)
run_title.font.bold = True
run_title.font.color.rgb = PRIMARY

# Subtitle
p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_sub.add_run('DevSecOps CI/CD Security & Monitoring Platform')
run_sub.font.name = 'Calibri'
run_sub.font.size = Pt(13)
run_sub.font.bold = True
run_sub.font.color.rgb = SECONDARY

# Metadata Table
meta_table = doc.add_table(rows=5, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ('Institution:', 'École Hassania des Travaux Publics (EHTP) — Casablanca'),
    ('Academic Program:', 'Computer Engineering Cycle (Cycle Ingénieur — Génie Informatique)'),
    ('Student:', 'AMHIDI Hamza'),
    ('GitHub Repository:', 'https://github.com/echoenvoy/SecOps-Pipeline'),
    ('Report Date:', 'October 07, 2026')
]
for idx, (label, val) in enumerate(meta_data):
    row = meta_table.rows[idx]
    c1, c2 = row.cells[0], row.cells[1]
    c1.width = Inches(1.8)
    c2.width = Inches(5.0)
    p1 = c1.paragraphs[0]
    r1 = p1.add_run(label)
    r1.font.bold = True
    r1.font.size = Pt(10)
    p2 = c2.paragraphs[0]
    r2 = p2.add_run(val)
    r2.font.size = Pt(10)
    set_cell_background(c1, 'F1F5F9')
    set_cell_background(c2, 'F8FAFC')

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 1: Previous Week (Phase 0)
h1 = doc.add_heading(level=1)
r_h1 = h1.add_run('1. Previous Week Accomplishments: Phase 0 (Environment & Repository Setup)')
r_h1.font.color.rgb = PRIMARY
r_h1.font.size = Pt(14)

doc.add_paragraph(
    'Phase 0 established the host development environment, container isolation network, local Kubernetes cluster, '
    'and modular repository architecture required for the complete DevSecOps pipeline.'
)

tasks_p0 = [
    ('Host Docker Daemon & Tools Verification: ', 'Started Docker Desktop on Windows/WSL2 and validated Docker Engine (v29.5.3) and Docker Compose (v5.1.4).'),
    ('Dedicated Security Container Network: ', 'Created private bridge network "devsecops-net" (Subnet: 172.20.0.0/16, Gateway: 172.20.0.1) for isolated cross-container communications between applications and future monitoring services (Wazuh, ELK, TheHive).'),
    ('Local Kubernetes Cluster Provisioning (kind): ', 'Installed kind CLI v0.33.0 via winget and deployed local cluster "devsecops-lab" (Kubernetes v1.37.0). Connected the control-plane container to "devsecops-net" (IP: 172.20.0.2). Verified node status as Ready via "kubectl get nodes".'),
    ('Modular Repository Scaffolding: ', 'Established directory layout matching all DevSecOps lifecycle stages (app/, docker/, k8s/, ci/, security/, monitoring/, ir/, docs/) with .gitkeep trackers.'),
    ('Governance & Workflow Automation: ', 'Configured comprehensive .gitignore, global architecture README.md, chronological tracking journal AVANCEMENT.md, contribution guidelines CONTRIBUTING.md, and GitHub PR/Issue templates enforcing the "Closes #<ID>" convention.')
]
for title, desc in tasks_p0:
    p = doc.add_paragraph(style='List Bullet')
    r_b = p.add_run(title)
    r_b.font.bold = True
    p.add_run(desc)

# Section 2: Today (Phase 1)
h2 = doc.add_heading(level=1)
r_h2 = h2.add_run('2. Today\'s Accomplishments: Phase 1 (Target Application & Dockerization)')
r_h2.font.color.rgb = PRIMARY
r_h2.font.size = Pt(14)

doc.add_paragraph(
    'Phase 1 designed, implemented, documented, and containerized the target web application with 5 intentional vulnerabilities '
    'for pre-deployment SAST verification and runtime intrusion detection.'
)

tasks_p1 = [
    ('Git Branching & Traceability: ', 'Created and checked out dedicated feature branch "feat/phase-1-target-app" following standard GitHub Flow.'),
    ('Target Web Microservice (app/): ', 'Built a Python/Flask web application backed by SQLite (devsecops.db) with test accounts (admin, alice, bob), confidential notes, and responsive HTML templates for visual testing.'),
    ('Intentional Vulnerabilities Implementation: ', 'Introduced 5 documented vulnerabilities across the codebase:\n'
     '  • VULN-01 (SQL Injection): Raw string concatenation in login and search queries (/api/search). Exploitable via "\' OR 1=1 --".\n'
     '  • VULN-02 (Reflected XSS): Dynamic unescaped template string rendering on /api/greet via Jinja2 "| safe".\n'
     '  • VULN-03 (Hardcoded Secrets): Static JWT and API keys embedded in app/config.py.\n'
     '  • VULN-04 (IDOR): Direct object reference on /api/notes/<id> without ownership verification.\n'
     '  • VULN-05 (Weak Cryptography): Obsolete MD5 hashing algorithm in password verification (/api/hash).'),
    ('Wazuh Runtime Telemetry & Logging: ', 'Implemented structured JSON authentication event logging ([AUTH_SUCCESS], [AUTH_FAILURE]) to feed runtime brute-force detection rules in Wazuh (Phase 6).'),
    ('Vulnerability Registry (docs/vulnerabilities.md): ', 'Documented all 5 vulnerabilities with CWE, OWASP Top 10 categories, file/line references, reproducible cURL PoC commands, and remediation instructions.'),
    ('Hardened Docker Containerization (docker/Dockerfile): ', 'Created a minimal container recipe using pinned python:3.12-slim, non-root user appuser (UID 1000), dependency caching with --no-cache-dir, built-in HEALTHCHECK on /health, and a .dockerignore file.'),
    ('Automated Testing & Container Verification: ', 'Built "target-app:dev", deployed to "devsecops-net", and ran automated test suite tests/test_endpoints.py inside the live container, achieving 100% test pass rate across all checks.'),
    ('Progress Tracking: ', 'Updated AVANCEMENT.md marking Phase 1 as COMPLETED, and committed deliverables to feat/phase-1-target-app.')
]
for title, desc in tasks_p1:
    p = doc.add_paragraph(style='List Bullet')
    r_b = p.add_run(title)
    r_b.font.bold = True
    p.add_run(desc)

# Section 3: Verification Matrix
h3 = doc.add_heading(level=1)
r_h3 = h3.add_run('3. Test & Verification Results Summary')
r_h3.font.color.rgb = PRIMARY
r_h3.font.size = Pt(14)

test_table = doc.add_table(rows=9, cols=4)
test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['Test Case / Verification', 'Target Endpoint / Command', 'Observed Result', 'Status']
for j, h in enumerate(headers):
    c = test_table.rows[0].cells[j]
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    set_cell_background(c, '0E7490')
    r.font.color.rgb = RGBColor(255, 255, 255)

matrix_data = [
    ('Container Healthcheck', 'GET /health', 'HTTP 200 {"status": "UP"}', 'PASS'),
    ('Non-Root Execution', 'docker exec whoami', 'Runs as unprivileged appuser (UID 1000)', 'PASS'),
    ('SQLi Auth Bypass', 'POST /api/login', "Bypassed authentication using admin' --", 'PASS'),
    ('SQLi Data Exfiltration', 'GET /api/search?q=\' OR 1=1 --', 'Extracted all database user records', 'PASS'),
    ('Reflected XSS', 'GET /api/greet?name=<script>...', 'Reflected unescaped JavaScript tags', 'PASS'),
    ('IDOR Access Violation', 'GET /api/notes/2', "Retrieved Bob's private note without session", 'PASS'),
    ('Weak Cryptography', 'POST /api/hash', 'Generated 32-char MD5 hex digest', 'PASS'),
    ('Wazuh Auth Telemetry', 'docker logs target-app', 'Emitted structured [AUTH_FAILURE] JSON', 'PASS')
]
for idx, (tc, ep, res, stat) in enumerate(matrix_data):
    row = test_table.rows[idx + 1]
    for col_idx, text in enumerate([tc, ep, res, stat]):
        c = row.cells[col_idx]
        p = c.paragraphs[0]
        r = p.add_run(text)
        r.font.size = Pt(9)
        if col_idx == 3:
            r.font.bold = True
            r.font.color.rgb = RGBColor(16, 185, 129) # Emerald Green
        if idx % 2 == 1:
            set_cell_background(c, 'F8FAFC')

# Section 4: Deliverables & Next Steps
h4 = doc.add_heading(level=1)
r_h4 = h4.add_run('4. Project Status & Next Steps (Phase 2)')
r_h4.font.color.rgb = PRIMARY
r_h4.font.size = Pt(14)

p_status = doc.add_paragraph()
p_status.add_run('Both Phase 0 and Phase 1 are fully validated. The project is prepared for ').font.size = Pt(10)
r_bold_p2 = p_status.add_run('Phase 2 — CI/CD Pipeline Skeleton')
r_bold_p2.font.bold = True
r_bold_p2.font.size = Pt(10)
p_status.add_run(', which will establish the multi-stage continuous integration pipeline (SAST -> Quality Gate -> Docker Build -> Kubernetes Deployment).').font.size = Pt(10)

output_paths = [
    r'c:\Users\Hamza\Downloads\projet s5\docs\Compte_Rendu_DevSecOps_Platform.docx',
    r'c:\Users\Hamza\Downloads\Compte_Rendu_DevSecOps_Platform.docx'
]
for out in output_paths:
    doc.save(out)
print('DOCX generated successfully at both locations.')

# Intentional Vulnerabilities Registry

This document catalogues all intentionally introduced vulnerabilities within the target web application (`app/`). It serves as the baseline ground-truth against which:
1. **Shift-Left SAST Scans** (Semgrep in Phase 3, SonarQube in Phase 4) will be evaluated.
2. **Shift-Right Runtime Detection** (Wazuh HIDS in Phase 6, ELK Stack in Phase 7) will trigger alerts.

---

## Vulnerability Summary Matrix

| ID | Vulnerability Type | OWASP Top 10 | Target File & Lines | Detection Stage | Expected Tool |
|---|---|---|---|---|---|
| **VULN-01** | SQL Injection (SQLi) | A03:2021 – Injection | `app/app.py` (L68, L114, L153, L175) | Pre-deployment SAST | Semgrep (`owasp-top-ten`) |
| **VULN-02** | Reflected Cross-Site Scripting (XSS) | A03:2021 – Injection | `app/app.py` (L190), `templates/index.html` (L21) | Pre-deployment SAST | Semgrep (`render-template-string`) |
| **VULN-03** | Hard-coded Secret & API Key | A07:2021 – Auth Failures | `app/config.py` (L8–L10), `app/app.py` (L22) | Code Review & SAST | Semgrep + SonarQube (Hotspot) |
| **VULN-04** | Insecure Direct Object Reference (IDOR) | A01:2021 – Broken Access Control | `app/app.py` (L81, L198–L204) | Runtime Log Anomaly | Wazuh rule + AI Anomaly |
| **VULN-05** | Weak Cryptographic Hash (MD5) | A02:2021 – Cryptographic Failures | `app/database.py` (L15), `app/app.py` (L214) | Code Quality Gate | SonarQube (`python:S4790`) |

---

## Detailed Vulnerability Profiles

### VULN-01: SQL Injection (SQLi)
- **CWE**: CWE-89 (Improper Neutralization of Special Elements used in an SQL Command)
- **Vulnerable Code Locations**:
  - `app/app.py`: Authentication query concatenation:
    ```python
    sql = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{hash_password_insecure(password)}'"
    cursor.execute(sql)
    ```
  - `app/app.py`: Search query concatenation:
    ```python
    sql = f"SELECT id, username, role, email FROM users WHERE username LIKE '%{query}%' OR email LIKE '%{query}%'"
    cursor.execute(sql)
    ```
- **Proof-of-Concept (Exploit Payload)**:
  ```bash
  # Bypass authentication
  curl -X POST http://localhost:8080/api/login \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"admin' --\", \"password\": \"anything\"}"

  # Extract users via search
  curl "http://localhost:8080/api/search?q='%20UNION%20SELECT%20id,username,role,email%20FROM%20users%20--"
  ```
- **Remediation**: Use parameterized queries (`cursor.execute("SELECT ... WHERE username = ?", (username,))`).

---

### VULN-02: Reflected Cross-Site Scripting (XSS)
- **CWE**: CWE-79 (Improper Neutralization of Input During Web Page Generation)
- **Vulnerable Code Location**:
  - `app/app.py`: Dynamic template string rendering:
    ```python
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)
    ```
  - `app/templates/index.html`: Disabling Jinja2 autoescaping:
    ```jinja2
    {{ greeting_html | safe }}
    ```
- **Proof-of-Concept (Exploit Payload)**:
  ```bash
  curl "http://localhost:8080/api/greet?name=%3Cscript%3Ealert('XSS')%3C/script%3E"
  ```
- **Remediation**: Use static HTML templates with standard Jinja2 context variables; never pass untrusted user input to `render_template_string` or filter through `| safe`.

---

### VULN-03: Hard-coded Secrets and API Keys
- **CWE**: CWE-798 (Use of Hard-coded Credentials)
- **Vulnerable Code Location**:
  - `app/config.py`:
    ```python
    SECRET_KEY = "supersecretkey12345-do-not-use-in-production"
    JWT_SECRET = "devsecops-jwt-token-secret-hardcoded-value"
    API_KEY = "insecure-test-api-key-never-use-in-prod-12345"
    ```
- **Risk**: Credentials baked into Git commits or container layers can be extracted by any unauthorized user or image scanner.
- **Remediation**: Load secrets dynamically from environment variables (`os.environ["SECRET_KEY"]`) backed by Kubernetes Secrets.

---

### VULN-04: Insecure Direct Object Reference (IDOR)
- **CWE**: CWE-639 (Authorization Bypass Through User-Controlled Key)
- **Vulnerable Code Location**:
  - `app/app.py`:
    ```python
    @app.route("/api/notes/<int:note_id>", methods=["GET"])
    def api_get_note(note_id: int):
        cursor.execute("SELECT id, user_id, title, content, is_private FROM notes WHERE id = ?", (note_id,))
    ```
- **Proof-of-Concept (Exploit Payload)**:
  ```bash
  # Authenticated as Alice (User ID 2), retrieve Bob's private financial note (Note ID 2):
  curl http://localhost:8080/api/notes/2
  ```
- **Remediation**: Enforce authorization checks validating `note['user_id'] == session.get('user_id')` or `session.get('role') == 'admin'`.

---

### VULN-05: Weak Cryptographic Hash Function (MD5)
- **CWE**: CWE-328 (Use of Weak Hash)
- **Vulnerable Code Location**:
  - `app/database.py`:
    ```python
    def hash_password_insecure(password: str) -> str:
        return hashlib.md5(password.encode("utf-8")).hexdigest()
    ```
- **Risk**: Susceptible to rainbow-table lookups and collision attacks.
- **Remediation**: Upgrade to `bcrypt` or `argon2` with salt.

---

## Runtime Telemetry: Authentication Logs for Wazuh

In addition to static vulnerabilities, the application produces structured authentication events designed for **Wazuh HIDS Rule Detection (Phase 6)**:

```text
2026-10-07 08:50:00 [INFO] [AUTH_FAILURE] user=admin ip=192.168.1.105 details=Invalid credentials json={"timestamp": "...", "event": "AUTH_FAILURE", "username": "admin", "src_ip": "192.168.1.105"}
2026-10-07 08:50:05 [INFO] [AUTH_SUCCESS] user=alice ip=192.168.1.105 details=role=user json={"timestamp": "...", "event": "AUTH_SUCCESS", "username": "alice", "src_ip": "192.168.1.105"}
```
- A burst of `[AUTH_FAILURE]` events will trigger the **Wazuh brute-force rule** (`rule.id: 100002`, `level >= 10`).
- Successive access to unauthorized note IDs will trigger the **IDOR/access anomaly rule**.

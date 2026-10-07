import os
import sys
import logging
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, render_template_string
from app.config import Config
from app.database import init_db, get_db_connection, hash_password_insecure

# Configure structured logging for Wazuh and ELK ingestion
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("secops-app")

app = Flask(__name__)
# INTENTIONAL VULNERABILITY (VULN-03): Hardcoded secret key assigned directly from Config
app.secret_key = Config.SECRET_KEY

# Ensure database is initialized on startup
with app.app_context():
    init_db()

def log_auth_event(event_type: str, username: str, ip: str, details: str = ""):
    """Emits structured audit log for Wazuh HIDS detection."""
    log_payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        "username": username,
        "src_ip": ip,
        "details": details
    }
    # Standard format: [AUTH_EVENT] {...json...}
    logger.info(f"[{event_type}] user={username} ip={ip} details={details} json={json.dumps(log_payload)}")


@app.route("/health", methods=["GET"])
def healthcheck():
    """Healthcheck endpoint for Kubernetes probes and Docker container status."""
    return jsonify({
        "status": "UP",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "target-app",
        "version": "1.0.0"
    }), 200


@app.route("/", methods=["GET"])
def index():
    """Home dashboard with interactive forms triggering the test vulnerabilities."""
    raw_name = request.args.get("name", "")
    greeting_html = None
    if raw_name:
        # INTENTIONAL VULNERABILITY (VULN-02): Reflected XSS
        greeting_html = f"<span>Hello, {raw_name}! Welcome to the platform.</span>"

    search_query = request.args.get("search", "")
    search_results = []
    if search_query:
        conn = get_db_connection()
        cursor = conn.cursor()
        # INTENTIONAL VULNERABILITY (VULN-01): SQL Injection via raw string formatting
        # Semgrep rule: python.lang.security.audit.sqli.format-string-sqli
        sql = f"SELECT id, username, role, email FROM users WHERE username LIKE '%{search_query}%' OR email LIKE '%{search_query}%'"
        try:
            cursor.execute(sql)
            search_results = [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            search_results = [{"id": 0, "username": "SQL_ERROR", "role": "error", "email": str(e)}]
        finally:
            conn.close()

    current_note_id = request.args.get("note_id", "")
    current_note = None
    if current_note_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        # INTENTIONAL VULNERABILITY (VULN-04): IDOR - No ownership check (missing: AND user_id = session['user_id'])
        cursor.execute("SELECT id, user_id, title, content FROM notes WHERE id = ?", (current_note_id,))
        row = cursor.fetchone()
        if row:
            current_note = dict(row)
        conn.close()

    return render_template(
        "index.html",
        raw_name=raw_name,
        greeting_html=greeting_html,
        search_query=search_query,
        search_results=search_results,
        current_note_id=current_note_id,
        current_note=current_note
    )


@app.route("/login", methods=["GET", "POST"])
def login_view():
    """Web login interface."""
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    client_ip = request.remote_addr or "127.0.0.1"

    conn = get_db_connection()
    cursor = conn.cursor()

    # INTENTIONAL VULNERABILITY (VULN-01): SQL Injection in authentication logic
    sql = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{hash_password_insecure(password)}'"
    try:
        cursor.execute(sql)
        user = cursor.fetchone()
    except Exception as e:
        log_auth_event("AUTH_FAILURE", username, client_ip, f"SQL_EXCEPTION: {str(e)}")
        conn.close()
        return render_template("login.html", error=f"Database error: {str(e)}")

    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        log_auth_event("AUTH_SUCCESS", username, client_ip, f"role={user['role']}")
        conn.close()
        return redirect(url_for("index"))
    else:
        # Crucial for Wazuh brute-force detection rule:
        log_auth_event("AUTH_FAILURE", username, client_ip, "Invalid credentials")
        conn.close()
        return render_template("login.html", error="Invalid username or password.")


@app.route("/logout", methods=["GET"])
def logout():
    """Clears user session."""
    session.clear()
    return redirect(url_for("index"))


# -------------------------------------------------------------
# REST API Endpoints
# -------------------------------------------------------------

@app.route("/api/login", methods=["POST"])
def api_login():
    """REST login endpoint emitting structured authentication logs."""
    data = request.get_json(silent=True) or request.form
    username = data.get("username", "")
    password = data.get("password", "")
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr or "127.0.0.1")

    conn = get_db_connection()
    cursor = conn.cursor()

    # INTENTIONAL VULNERABILITY (VULN-01): SQL Injection in REST API
    sql = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{hash_password_insecure(password)}'"
    try:
        cursor.execute(sql)
        user = cursor.fetchone()
    except Exception as e:
        log_auth_event("AUTH_FAILURE", username, client_ip, f"SQL_ERROR: {str(e)}")
        conn.close()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    if user:
        log_auth_event("AUTH_SUCCESS", username, client_ip, f"role={user['role']}")
        conn.close()
        return jsonify({
            "status": "success",
            "message": "Authentication successful",
            "user": {"id": user["id"], "username": user["username"], "role": user["role"]}
        }), 200
    else:
        log_auth_event("AUTH_FAILURE", username, client_ip, "Invalid credentials")
        conn.close()
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401


@app.route("/api/search", methods=["GET"])
def api_search():
    """REST search endpoint demonstrating SQL Injection."""
    query = request.args.get("q", "")
    conn = get_db_connection()
    cursor = conn.cursor()

    # INTENTIONAL VULNERABILITY (VULN-01): SQL Injection via raw query concatenation
    sql = f"SELECT id, username, role, email FROM users WHERE username LIKE '%{query}%' OR email LIKE '%{query}%'"
    try:
        cursor.execute(sql)
        results = [dict(row) for row in cursor.fetchall()]
        return jsonify({"query": query, "count": len(results), "results": results}), 200
    except Exception as e:
        return jsonify({"error": "SQL Syntax Error", "details": str(e)}), 500
    finally:
        conn.close()


@app.route("/api/greet", methods=["GET"])
def api_greet():
    """REST endpoint demonstrating Reflected XSS."""
    name = request.args.get("name", "Guest")
    # INTENTIONAL VULNERABILITY (VULN-02): Dynamic template string rendering without sanitization
    # Semgrep rule: python.flask.security.audit.render-template-string.render-template-string
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)


@app.route("/api/notes/<int:note_id>", methods=["GET"])
def api_get_note(note_id: int):
    """
    REST endpoint demonstrating IDOR (Insecure Direct Object Reference).
    INTENTIONAL VULNERABILITY (VULN-04): Retrieves record without verifying caller ownership.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, title, content, is_private FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"note": dict(note)}), 200


@app.route("/api/hash", methods=["POST"])
def api_hash():
    """
    REST endpoint demonstrating weak cryptography.
    INTENTIONAL VULNERABILITY (VULN-05): MD5 hashing for passwords.
    """
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    return jsonify({
        "algorithm": "MD5",
        "hash": hash_password_insecure(text)
    }), 200


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

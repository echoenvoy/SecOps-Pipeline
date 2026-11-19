"""
Remediated Target Application (Clean Reference for SAST Verification)
Domain: DevSecOps CI/CD Security & Monitoring Platform
Ref: Specification Document Section 5.2 (Demonstrating pipeline pass after remediation)
"""
from flask import Flask, request, jsonify, render_template, session
from config import Config
from database import get_db_connection, hash_password_secure, init_db

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({"status": "UP", "version": "1.0.0-remediated"}), 200

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    # REMEDIATED: Parameterized SQL query preventing SQL Injection (VULN-01)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, role FROM users WHERE username = ? AND password = ?",
        (username, hash_password_secure(password))
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Authentication successful", "role": user["role"]}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/search", methods=["GET"])
def api_search():
    query = request.args.get("q", "")
    conn = get_db_connection()
    cursor = conn.cursor()

    # REMEDIATED: Parameterized search query preventing SQL Injection (VULN-01)
    search_param = f"%{query}%"
    cursor.execute(
        "SELECT id, username, role, email FROM users WHERE username LIKE ? OR email LIKE ?",
        (search_param, search_param)
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"query": query, "count": len(results), "results": results}), 200

@app.route("/api/greet", methods=["GET"])
def api_greet():
    name = request.args.get("name", "Guest")
    # REMEDIATED: Uses standard JSON or template with autoescaping, not render_template_string (VULN-02)
    return jsonify({"greeting": f"Hello, {name}!"}), 200

@app.route("/api/notes/<int:note_id>", methods=["GET"])
def api_get_note(note_id: int):
    # REMEDIATED: Enforces session-based ownership validation preventing IDOR (VULN-04)
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, title, content, is_private FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    if note["is_private"] and note["user_id"] != current_user_id:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify({"note": dict(note)}), 200

@app.route("/api/hash", methods=["POST"])
def api_hash():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    # REMEDIATED: Uses SHA-256 secure hash (VULN-05)
    return jsonify({
        "algorithm": "SHA-256",
        "hash": hash_password_secure(text)
    }), 200

if __name__ == "__main__":
    init_db()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

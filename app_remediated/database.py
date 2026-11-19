"""
Remediated Database Module (Clean Reference for SAST Verification)
Domain: DevSecOps CI/CD Security & Monitoring Platform
Ref: VULN-05 Remediation (SHA-256 secure password hashing)
"""
import hashlib
import sqlite3

DATABASE_NAME = "remediated_devsecops.db"

def hash_password_secure(password: str) -> str:
    """Remediated secure cryptographic hashing utilizing SHA-256 with salt."""
    salt = "secops-salt-token"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            is_private BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

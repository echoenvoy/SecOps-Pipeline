import sqlite3
import hashlib
from app.config import Config

def get_db_connection():
    """Returns a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password_insecure(password: str) -> str:
    """
    INTENTIONAL VULNERABILITY (VULN-05): Weak Cryptographic Hash (MD5)
    Semgrep rule: python.lang.security.insecure-hash-algorithm-md5.insecure-hash-algorithm-md5
    SonarQube rule: python:S4790 (Weak hashing algorithms like MD5/SHA1 should not be used)
    """
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def init_db():
    """Initializes database schema and populates seed data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        email TEXT
    );
    """)
    
    # Create Notes table (used for IDOR demonstration)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        is_private INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)
    
    # Create Audit Logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        event_type TEXT NOT NULL,
        username TEXT,
        ip_address TEXT,
        details TEXT
    );
    """)
    
    # Seed default users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users = [
            ("admin", hash_password_insecure("admin123"), "admin", "admin@devsecops.local"),
            ("alice", hash_password_insecure("alice123"), "user", "alice@devsecops.local"),
            ("bob", hash_password_insecure("bob123"), "user", "bob@devsecops.local")
        ]
        cursor.executemany("INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)", users)
        
        # Seed notes
        notes = [
            (2, "Alice's Private Project Roadmap", "Confidential DevSecOps automation roadmap for 2026-2027.", 1),
            (3, "Bob's Financial Payroll Audit", "Q3 Salary details and internal accounting credentials.", 1),
            (1, "System Security Master Keys", "Root API tokens and internal cluster service account hashes.", 1)
        ]
        cursor.executemany("INSERT INTO notes (user_id, title, content, is_private) VALUES (?, ?, ?, ?)", notes)
    
    conn.commit()
    conn.close()

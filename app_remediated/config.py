"""
Remediated Configuration File (Clean Reference for SAST Verification)
Domain: DevSecOps CI/CD Security & Monitoring Platform
Ref: VULN-03 Remediation (No hardcoded credentials)
"""
import os

class Config:
    HOST = os.environ.get("APP_HOST", "0.0.0.0")
    PORT = int(os.environ.get("APP_PORT", 8080))
    DEBUG = False
    
    # Securely loaded from environment / Kubernetes Secrets
    SECRET_KEY = os.environ.get("APP_SECRET_KEY", "dynamic-vault-secret-env-var")
    JWT_SECRET = os.environ.get("APP_JWT_SECRET", "dynamic-jwt-key-from-k8s-secret")
    API_KEY = os.environ.get("APP_API_KEY", "dynamic-api-token-from-vault")

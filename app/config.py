import os

class Config:
    """Application configuration containing intentional vulnerabilities for SAST detection."""
    
    # INTENTIONAL VULNERABILITY (VULN-03): Hard-coded secret key and API token
    # Semgrep rule: generic.secrets.security.detected-jwt-secret / hardcoded-secret
    # SonarQube rule: python:S2068 (Credentials should not be hard-coded)
    SECRET_KEY = "supersecretkey12345-do-not-use-in-production"
    JWT_SECRET = "devsecops-jwt-token-secret-hardcoded-value"
    API_KEY = "insecure-test-api-key-never-use-in-prod-12345"
    
    # Debug mode enabled in configuration
    DEBUG = True
    
    # Database
    DATABASE_PATH = os.environ.get("DATABASE_PATH", "devsecops.db")
    
    # Host & Port
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 8080))

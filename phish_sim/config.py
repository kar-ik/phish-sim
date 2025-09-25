import os
from pathlib import Path

SANDBOX_MODE = os.getenv("PHISH_SANDBOX", "true").lower() == "true"
SENDGRID_ENABLED = False  
RETENTION_DAYS = 30
DB_PATH = Path("db.sqlite")
LOGS_PATH = Path("logs/audit.json")
CONSENT_DIR = Path("consent_files")
TEMPLATES_DIR = Path("phish_sim/templates")

BANNED_TOKENS = ["password", "ssn", "pin", "otp", "credential", "login"]

USERS = {"admin": "admin_pass", "manager": "manager_pass"}  

KILL_SWITCH = False

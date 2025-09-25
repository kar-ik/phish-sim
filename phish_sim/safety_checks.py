import re

BANNED_TOKENS = ["password", "ssn", "pin", "otp", "credential", "login"] 

def scan_template(body_html):
    warnings = []
    for token in BANNED_TOKENS:
        if re.search(token, body_html, re.IGNORECASE):
            warnings.append(f"Risky token: {token}")
    return warnings

def validate_landing_page(html, allowed_fields):
    if re.search(r'<input.*type=["\']password["\']', html, re.IGNORECASE):
        raise ValueError("Password fields blocked!")
    if "password" in allowed_fields:
        raise ValueError("Password fields not allowed.")
    return True

def check_dangerous_config(scope, domains):
    if "external" in domains or len(scope) > 100:  
        raise ValueError("Dangerous config: External domains or mass send detected.")

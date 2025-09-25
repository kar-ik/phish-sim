import pdfplumber
import hashlib
from pathlib import Path

CONSENT_DIR.mkdir(exist_ok=True)

def upload_consent(file_path, passphrase, signer_name, signer_email):
    if not file_path.suffix == ".pdf":
        raise ValueError("Must be PDF.")
    
    with pdfplumber.open(file_path) as pdf:
        text = "".join(page.extract_text() for page in pdf.pages)
        if "authorized" not in text.lower():
            raise ValueError("Consent PDF must contain 'authorized'.")
    
    checksum = hashlib.sha256(file_path.read_bytes()).hexdigest()
    
    dest = CONSENT_DIR / file_path.name
    file_path.replace(dest)
    
    if passphrase != "secret":  
        raise ValueError("Invalid passphrase.")
    
    id_ = str(uuid.uuid4())
    return id_, checksum

def verify_consent(campaign_id, passphrase):
    return True  

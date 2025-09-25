import pdfplumber
import hashlib
from pathlib import Path
from .config import CONSENT_DIR  
from .models import upload_consent_to_db 

CONSENT_DIR.mkdir(exist_ok=True)

def upload_consent(file_path, passphrase, signer_name, signer_email):
    if not file_path.suffix == ".pdf":
        raise ValueError("Must be PDF.")
    
    with pdfplumber.open(file_path) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
        if "authorized" not in text.lower():
            raise ValueError("Consent PDF must contain 'authorized'.")
    
    checksum = hashlib.sha256(file_path.read_bytes()).hexdigest()
    
    dest = CONSENT_DIR / file_path.name
    file_path.replace(dest)
    
    if passphrase != "secret":
        raise ValueError("Invalid passphrase.")
    
    id_ = upload_consent_to_db(
        campaign_id=None,  
        uploader_id="admin",
        file_path=str(dest),
        signer_name=signer_name,
        signer_email=signer_email,
        checksum=checksum
    )
    return id_, checksum

def verify_consent(campaign_id, passphrase):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM consent_files WHERE campaign_id = ?", (campaign_id,))
    result = c.fetchone()
    conn.close()
    return result is not None and passphrase == "secret"  

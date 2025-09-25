import sqlite3
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
import json

DB_PATH = Path("phish_sim/config.py").parent / "db.sqlite"  

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            owner_id TEXT,
            start_time TEXT,
            end_time TEXT,
            status TEXT DEFAULT 'draft',
            consent_file_id TEXT,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id TEXT PRIMARY KEY,
            campaign_id TEXT,
            name TEXT,
            subject TEXT,
            body_html TEXT,
            blocked_tokens TEXT,  -- JSON array
            approved BOOLEAN DEFAULT FALSE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS landing_pages (
            id TEXT PRIMARY KEY,
            campaign_id TEXT,
            html TEXT,
            allowed_fields TEXT,  -- JSON list, no 'password'
            show_mock_banner BOOLEAN DEFAULT TRUE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id TEXT PRIMARY KEY,
            email_hash TEXT,
            display_name TEXT,
            opted_in BOOLEAN DEFAULT FALSE,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            campaign_id TEXT,
            participant_id TEXT,
            event_type TEXT,  -- delivered/opened/clicked/submitted/reported
            timestamp TEXT,
            meta TEXT  -- JSON, no values
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            action TEXT,
            details TEXT,
            timestamp TEXT,
            prev_hash TEXT,
            cur_hash TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS consent_files (
            id TEXT PRIMARY KEY,
            campaign_id TEXT,
            uploader_id TEXT,
            file_path TEXT,
            signer_name TEXT,
            signer_email TEXT,
            signed_date TEXT,
            checksum TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_campaign(name, description, owner_id, consent_file_id):
    id_ = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO campaigns (id, name, description, owner_id, consent_file_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_, name, description, owner_id, consent_file_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return id_

def log_event(campaign_id, participant_id, event_type, meta={}):
    id_ = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (id, campaign_id, participant_id, event_type, timestamp, meta)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_, campaign_id, participant_id, event_type, datetime.now().isoformat(), json.dumps(meta)))
    conn.commit()
    conn.close()

def hash_email(email):
    return hashlib.sha256(email.encode()).hexdigest()

def purge_old_data():
    cutoff = datetime.now().timestamp() - (RETENTION_DAYS * 86400)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE timestamp < ?", (cutoff,))
    conn.commit()
    conn.close()

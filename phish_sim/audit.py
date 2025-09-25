import json
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

LOGS_PATH.parent.mkdir(exist_ok=True)

def log_action(user_id, action, details):
    entry = {
        "user_id": user_id,
        "action": action,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    try:
        with open(LOGS_PATH, "r") as f:
            logs = json.load(f)
        prev_hash = logs[-1]["cur_hash"] if logs else None
    except FileNotFoundError:
        logs = []
        prev_hash = None
    
    entry_str = json.dumps(entry, sort_keys=True)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(entry_str.encode())
    cur_hash = digest.finalize().hex()
    
    entry["prev_hash"] = prev_hash
    entry["cur_hash"] = cur_hash
    
    logs.append(entry)
    with open(LOGS_PATH, "w") as f:
        json.dump(logs, f)

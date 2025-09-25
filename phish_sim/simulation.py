import random
from datetime import datetime, timedelta

def run_simulation(campaign_id, seed_accounts):
    random.seed(42)  
    events = []
    for email in seed_accounts:
        participant_id = hash_email(email)  
        log_event(campaign_id, participant_id, "delivered")
        if random.random() > 0.5:  
            log_event(campaign_id, participant_id, "opened")
            if random.random() > 0.3:  
                log_event(campaign_id, participant_id, "clicked")
                if random.random() > 0.2:  
                    log_event(campaign_id, participant_id, "submitted")
    return {"metrics": {"delivered": len(seed_accounts), "opened": sum(1 for e in events if e["type"]=="opened")}}  

def generate_report(campaign_id):
    return {"stats": "Anonymized funnel chart data"}

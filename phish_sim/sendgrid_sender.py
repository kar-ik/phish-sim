import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from phish_sim.config import SENDGRID_ENABLED

def send_real_email(to_email, subject, html_body, api_key):
    if not SENDGRID_ENABLED:
        raise ValueError("SendGrid disabled. Use --enable-sendgrid after admin approval.")
    
    sg = SendGridAPIClient(api_key)
    message = Mail(
        from_email='your-org@domain.com',  
        to_emails=to_email,
        subject=subject,
        html_content=html_body.replace("{{link}}", "http://localhost/sim-landing")  
    )
    response = sg.send(message)
    if response.status_code != 202:
        raise ValueError("Send failed.")
    return True

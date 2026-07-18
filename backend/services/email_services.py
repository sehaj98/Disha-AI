import os
import requests

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
SENDER_NAME = "Disha AI"

BREVO_URL = "https://api.brevo.com/v3/smtp/email"


def send_update_email(to_email: str, to_name: str, digest: str) -> bool:
    """Sends the digest as an email via Brevo's REST API.
    Returns True/False instead of raising, so one bad send never crashes
    the scheduler loop for the rest of the students."""
    if not BREVO_API_KEY or not SENDER_EMAIL:
        print("Email not sent: missing BREVO_API_KEY or BREVO_SENDER_EMAIL in .env")
        return False

    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": to_email, "name": to_name or to_email}],
        "subject": "Your Disha AI update",
        "htmlContent": f"""
            <div style="font-family: sans-serif; max-width: 560px; margin: 0 auto;">
                <h2 style="color:#12142b;">Hi {to_name or 'there'},</h2>
                <p style="color:#333; line-height:1.6;">{digest}</p>
                <p style="color:#888; font-size:12px; margin-top:32px;">
                    You're receiving this because you signed up for Disha AI updates.
                </p>
            </div>
        """,
    }
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        res = requests.post(BREVO_URL, json=payload, headers=headers, timeout=15)
        if res.status_code >= 300:
            print("Brevo error:", res.status_code, res.text)
            return False
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False
        
import os
from datetime import date, timedelta

from database import SessionLocal
import models
from services.updates_service import get_updates_for_student
from services.email_service import send_update_email

# How many days between emails for a given student. Change this in .env
# to control the "particular timing period" — e.g. 7 for weekly, 3 for
# every three days. It's per-student due-checking, not a fixed clock time.
EMAIL_INTERVAL_DAYS = int(os.getenv("EMAIL_INTERVAL_DAYS", "7"))


def send_due_updates():
    """Runs on a schedule (see main.py). For every student who has never
    been emailed, or whose last email was more than EMAIL_INTERVAL_DAYS
    ago, generates a fresh digest and sends it, then stamps
    last_emailed_at so they aren't emailed again until the next window."""
    db = SessionLocal()
    try:
        students = db.query(models.Student).all()
        cutoff = date.today() - timedelta(days=EMAIL_INTERVAL_DAYS)

        for student in students:
            due = student.last_emailed_at is None or student.last_emailed_at <= cutoff
            if not due:
                continue

            digest = get_updates_for_student(student)
            sent = send_update_email(student.email, student.name, digest)

            if sent:
                student.last_emailed_at = date.today()
                db.add(student)

        db.commit()
    finally:
        db.close()
        
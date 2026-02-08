"""SMS/Email notification sender for water service alerts.

TODO: implement batching and retry logic (see AGENTS.md)
"""
import time
import json
import logging
from priority import prioritized_residents

SMS_RATE_LIMIT = 50  # messages per minute
LOG_FILE = "notifications.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


def send_sms(phone, message):
    """Send SMS via provider API. Returns True on success."""
    # TODO: replace with actual API call
    # provider: Twilio account is in 1Password under "water-dept-sms"
    print(f"[SMS] {phone}: {message}")
    return True


def send_email(email, subject, body):
    """Send email notification. Returns True on success."""
    # TODO: hook up SMTP (see config in /etc/water-notify/smtp.conf)
    print(f"[EMAIL] {email}: {subject}")
    return True


def send_notifications(alert_type, message):
    """Send notifications to all residents in priority order.

    TODO:
    - batch by tier (tier 1 first, then 2, then 3)
    - respect SMS_RATE_LIMIT (50/min)
    - retry logic: tier 1 gets 3 retries with exponential backoff,
      tier 2-3 get 1 retry
    - log failures
    """
    residents = prioritized_residents()

    for resident in residents:
        phone = resident.get("phone")
        email = resident.get("email")

        if phone:
            send_sms(phone, message)
        if email:
            send_email(email, f"Water Alert: {alert_type}", message)


if __name__ == "__main__":
    send_notifications(
        "Boil Advisory",
        "A boil-water advisory is in effect for your area. Boil all water for at least 1 minute before drinking."
    )

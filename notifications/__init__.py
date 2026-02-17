# Notification engine for SMS and Email

from typing import Any

class NotificationEngine:
    """
    Handles sending notifications via SMS and Email.
    Methods can be expanded to integrate with real gateways.
    """
    def send_sms(self, phone_number: str, message: str) -> Any:
        # Simulate sending an SMS
        print(f"SMS sent to {phone_number}: {message}")
        return {"status": "sent", "type": "sms"}

    def send_email(self, email: str, subject: str, body: str) -> Any:
        # Simulate sending an Email
        print(f"Email sent to {email}: {subject} - {body}")
        return {"status": "sent", "type": "email"}

from typing import Any

class NotificationEngine:
    """
    Handles sending notifications via SMS and Email.
    Methods can be expanded to integrate with real gateways.
    """
    def send_sms(self, phone_number: str, message: str) -> Any:
        print(f"SMS sent to {phone_number}: {message}")
        return {"status": "sent", "type": "sms"}

    def send_email(self, email: str, subject: str, body: str) -> Any:
        print(f"Email sent to {email}: {subject} - {body}")
        return {"status": "sent", "type": "email"}

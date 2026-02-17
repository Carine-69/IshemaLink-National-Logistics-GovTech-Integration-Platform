from typing import Dict, Any

# Payment gateway logic and adapters (e.g., MomoMock)

class MomoMock:
    """
    Simulates MTN/Airtel Mobile Money payment gateway for testing.
    Provides methods to initiate payment and simulate webhook callbacks.
    """
    def initiate_payment(self, amount: float, phone_number: str, reference: str) -> Dict[str, Any]:
        # Simulate sending a mobile money push prompt
        return {
            "status": "pending",
            "transaction_id": f"MOCK-{reference}",
            "message": "Payment prompt sent to user."
        }

    def simulate_webhook(self, transaction_id: str, success: bool = True) -> Dict[str, Any]:
        # Simulate a webhook callback from the mobile money provider
        return {
            "transaction_id": transaction_id,
            "status": "success" if success else "failed",
            "message": "Payment processed by MomoMock."
        }

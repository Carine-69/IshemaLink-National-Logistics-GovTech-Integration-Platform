from typing import Dict, Any

class MomoMock:
    """
    Simulates MTN/Airtel Mobile Money payment gateway for testing.
    Provides methods to initiate payment and simulate webhook callbacks.
    """
    def initiate_payment(self, amount: float, phone_number: str, reference: str) -> Dict[str, Any]:
        return {
            "status": "pending",
            "transaction_id": f"MOCK-{reference}",
            "message": "Payment prompt sent to user."
        }

    def simulate_webhook(self, transaction_id: str, success: bool = True) -> Dict[str, Any]:
        return {
            "transaction_id": transaction_id,
            "status": "success" if success else "failed",
            "message": "Payment processed by MomoMock."
        }

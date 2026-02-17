from typing import Any, Dict, Optional
from payments import MomoMock
from notifications import NotificationEngine
from django.db import transaction

# BookingService orchestrates the unified booking/payment/dispatch flow

class BookingService:
    """
    Orchestrates the unified booking, payment, and dispatch workflow.
    - Handles Domestic and International logic
    - Integrates with Payment and Notification services via dependency injection
    - Ensures ACID compliance using atomic transactions
    - Supports async payment callbacks
    """
    def __init__(self, payment_gateway: MomoMock, notifier: NotificationEngine):
        self.payment_gateway = payment_gateway
        self.notifier = notifier

    @transaction.atomic
    def create_shipment(self, shipment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Unified Booking Flow:
        1. Create shipment (Domestic/Intl)
        2. Calculate tariff
        3. Request payment
        4. Assign driver (after payment)
        """
        # 1. Create shipment (call Domestic/International logic)
        shipment_type = shipment_data.get("type", "domestic")
        if shipment_type == "domestic":
            # Placeholder: Call Domestic module logic
            shipment_id = "DOM-12345"
        else:
            # Placeholder: Call International module logic
            shipment_id = "INT-12345"

        # 2. Calculate tariff (placeholder logic)
        weight = shipment_data.get("weight", 1)
        base_tariff = 1000 if shipment_type == "domestic" else 3000
        tariff = base_tariff * weight

        # 3. Request payment (initiate Mobile Money)
        phone_number = shipment_data.get("phone_number", "0780000000")
        payment_response = self.payment_gateway.initiate_payment(
            amount=tariff,
            phone_number=phone_number,
            reference=shipment_id
        )

        # 4. Return response (awaiting payment confirmation)
        return {
            "status": "pending_payment",
            "shipment_id": shipment_id,
            "tariff": tariff,
            "payment": payment_response
        }

    def handle_payment_callback(self, payment_result: Dict[str, Any]) -> None:
        """
        Handles async payment webhook/callback.
        If payment is successful, confirms booking and assigns driver.
        If failed, rolls back booking and notifies user.
        """
        transaction_id = payment_result.get("transaction_id")
        status = payment_result.get("status")
        # Simulate shipment lookup by transaction_id (in real code, query DB)
        shipment_id = transaction_id.replace("MOCK-", "") if transaction_id else None
        if status == "success":
            # Assign driver (placeholder logic)
            assigned_driver = "DRIVER-001"
            # Send notifications
            self.notifier.send_sms(
                phone_number="0780000000",  # In real code, fetch from shipment
                message=f"Your shipment {shipment_id} is confirmed. Driver: {assigned_driver}"
            )
            self.notifier.send_email(
                email="exporter@example.com",  # In real code, fetch from shipment
                subject="Shipment Confirmed",
                body=f"Your shipment {shipment_id} is confirmed and assigned to driver {assigned_driver}."
            )
            # Update shipment status in DB (placeholder)
            print(f"Shipment {shipment_id} confirmed and driver assigned.")
        else:
            # Rollback booking (placeholder)
            print(f"Payment failed for shipment {shipment_id}. Rolling back booking.")
            self.notifier.send_sms(
                phone_number="0780000000",
                message=f"Payment failed for shipment {shipment_id}. Please try again."
            )

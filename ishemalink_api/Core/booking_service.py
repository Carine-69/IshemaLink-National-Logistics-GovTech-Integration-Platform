from typing import Any, Dict, Optional
from payments import MomoMock
from notifications import NotificationEngine
from django.db import transaction
from Core.models import Shipment, Driver

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
        shipment_type = shipment_data.get("type", "domestic")
        weight = shipment_data.get("weight", 1)
        phone_number = shipment_data.get("phone_number", "0780000000")
        base_tariff = 1000 if shipment_type == "domestic" else 3000
        tariff = base_tariff * weight
        # Create shipment in DB
        shipment = Shipment.objects.create(
            shipment_type=shipment_type,
            weight=weight,
            phone_number=phone_number,
            tariff=tariff,
            status="pending_payment"
        )
        payment_response = self.payment_gateway.initiate_payment(
            amount=tariff,
            phone_number=phone_number,
            reference=str(shipment.id)
        )
        return {
            "status": "pending_payment",
            "shipment_id": shipment.id,
            "tariff": tariff,
            "payment": payment_response
        }

    def handle_payment_callback(self, payment_result: Dict[str, Any]) -> None:
        transaction_id = payment_result.get("transaction_id")
        status = payment_result.get("status")
        # shipment_id is the DB id
        try:
            shipment_id = int(transaction_id.replace("MOCK-", ""))
            shipment = Shipment.objects.get(id=shipment_id)
        except Exception:
            print("Shipment not found for transaction_id", transaction_id)
            return
        if status == "success":
            # Assign first available driver
            driver = Driver.objects.filter(is_available=True).first()
            if driver:
                shipment.assigned_driver = driver
                shipment.status = "confirmed"
                driver.is_available = False
                driver.save()
                shipment.save()
                self.notifier.send_sms(
                    phone_number=shipment.phone_number,
                    message=f"Your shipment {shipment.id} is confirmed. Driver: {driver.name}"
                )
                self.notifier.send_email(
                    email="exporter@example.com",
                    subject="Shipment Confirmed",
                    body=f"Your shipment {shipment.id} is confirmed and assigned to driver {driver.name}."
                )
                print(f"Shipment {shipment.id} confirmed and driver {driver.name} assigned.")
            else:
                shipment.status = "confirmed_no_driver"
                shipment.save()
                print(f"Shipment {shipment.id} confirmed but no driver available.")
        else:
            shipment.status = "payment_failed"
            shipment.save()
            self.notifier.send_sms(
                phone_number=shipment.phone_number,
                message=f"Payment failed for shipment {shipment.id}. Please try again."
            )

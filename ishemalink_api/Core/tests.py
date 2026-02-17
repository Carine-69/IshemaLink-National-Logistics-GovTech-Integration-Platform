from django.test import TestCase, Client
from Core.models import Driver, Shipment

class BookingFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        Driver.objects.create(name="Test Driver", phone_number="0780000000", license_number="RWA12345", is_available=True)

    def test_create_shipment_and_payment(self):
        response = self.client.post("/api/shipments/create/", data={
            "type": "domestic",
            "weight": 2,
            "phone_number": "0781234567"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        shipment_id = response.json()["shipment_id"]
        # Simulate payment callback
        response2 = self.client.post("/api/payments/webhook/", data={
            "transaction_id": f"MOCK-{shipment_id}",
            "status": "success"
        }, content_type="application/json")
        self.assertEqual(response2.status_code, 200)
        shipment = Shipment.objects.get(id=shipment_id)
        self.assertEqual(shipment.status, "confirmed")
        self.assertIsNotNone(shipment.assigned_driver)

from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.license_number})"

class Shipment(models.Model):
    SHIPMENT_TYPE_CHOICES = [
        ("domestic", "Domestic"),
        ("international", "International"),
    ]
    shipment_type = models.CharField(max_length=20, choices=SHIPMENT_TYPE_CHOICES)
    weight = models.FloatField()
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=30, default="pending_payment")
    tariff = models.FloatField(default=0)
    assigned_driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shipment_type} - {self.id}"

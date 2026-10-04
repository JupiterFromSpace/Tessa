import uuid
from django.db import models
from providers.models import ProviderProfile


class Vehicle(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    class Transmission(models.TextChoices):
        AUTOMATIC = "automatic", "Automatic"
        MANUAL = "manual", "Manual"

    class FuelType(models.TextChoices):
        PETROL = "petrol", "Petrol"
        DIESEL = "diesel", "Diesel"
        HYBRID = "hybrid", "Hybrid"
        ELECTRIC = "electric", "Electric"

    class Category(models.TextChoices):
        ECONOMY = "economy", "Economy"
        SEDAN = "sedan", "Sedan"
        SUV = "suv", "SUV"
        LUXURY = "luxury", "Luxury"
        VAN = "van", "Van"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="vehicles")
    title = models.CharField(max_length=150)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=Category.choices)
    city = models.CharField(max_length=100, db_index=True)
    pickup_address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    seats = models.PositiveSmallIntegerField(default=5)
    transmission = models.CharField(max_length=20, choices=Transmission.choices)
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices)
    daily_price = models.PositiveBigIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class VehicleImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vehicles/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image - {self.vehicle.title}"

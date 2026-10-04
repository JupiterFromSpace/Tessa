import uuid
from django.conf import settings
from django.db import models


class ProviderProfile(models.Model):
    class VerificationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="provider_profile")
    national_id = models.CharField(max_length=20)
    driver_license_number = models.CharField(max_length=50)
    national_card_image = models.ImageField(upload_to="providers/national_cards/")
    driver_license_image = models.ImageField(upload_to="providers/driver_licenses/")
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.verification_status}"

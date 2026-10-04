from rest_framework import serializers
from .models import ProviderProfile


class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = (
            "id",
            "national_id",
            "driver_license_number",
            "national_card_image",
            "driver_license_image",
            "verification_status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "verification_status", "created_at", "updated_at")

    def create(self, validated_data):
        return ProviderProfile.objects.create(user=self.context["request"].user, **validated_data)

from rest_framework import serializers
from .models import Vehicle, VehicleImage


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ("id", "image", "created_at")
        read_only_fields = ("id", "created_at")


class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    provider_name = serializers.CharField(source="provider.user.get_full_name", read_only=True)

    class Meta:
        model = Vehicle
        fields = (
            "id", "title", "brand", "model", "year", "category", "city",
            "pickup_address", "description", "seats", "transmission", "fuel_type",
            "daily_price", "status", "provider_name", "images", "created_at", "updated_at",
        )
        read_only_fields = ("id", "provider_name", "images", "created_at", "updated_at")

    def validate(self, attrs):
        provider = getattr(self.context["request"].user, "provider_profile", None)
        if not provider or provider.verification_status != "approved":
            raise serializers.ValidationError("Your provider profile must be approved first.")
        return attrs

    def create(self, validated_data):
        return Vehicle.objects.create(provider=self.context["request"].user.provider_profile, **validated_data)


class VehicleImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ("id", "image", "created_at")
        read_only_fields = ("id", "created_at")

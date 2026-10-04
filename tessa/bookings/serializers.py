from datetime import date
from rest_framework import serializers
from .models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "vehicle", "start_date", "end_date", "note", "daily_price", "total_price", "status", "created_at")
        read_only_fields = ("id", "daily_price", "total_price", "status", "created_at")

    def validate(self, attrs):
        if attrs["start_date"] < date.today():
            raise serializers.ValidationError({"start_date": "Start date cannot be in the past."})
        if attrs["end_date"] <= attrs["start_date"]:
            raise serializers.ValidationError({"end_date": "End date must be after start date."})
        if attrs["vehicle"].status != "active":
            raise serializers.ValidationError("This vehicle is not available for booking.")
        if attrs["vehicle"].provider.verification_status != "approved":
            raise serializers.ValidationError("This vehicle provider is not approved.")
        return attrs


class BookingSerializer(serializers.ModelSerializer):
    vehicle_title = serializers.CharField(source="vehicle.title", read_only=True)
    vehicle_city = serializers.CharField(source="vehicle.city", read_only=True)
    renter_email = serializers.EmailField(source="renter.email", read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id", "vehicle", "vehicle_title", "vehicle_city", "renter_email",
            "start_date", "end_date", "daily_price", "total_price", "note",
            "status", "created_at", "updated_at",
        )

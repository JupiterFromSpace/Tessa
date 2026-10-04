from django.db import transaction
from django.db.models import Q
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer


ACTIVE_STATUSES = [Booking.Status.PENDING, Booking.Status.APPROVED]


class BookingListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(renter=self.request.user).select_related("vehicle", "renter")

    def get_serializer_class(self):
        return BookingCreateSerializer if self.request.method == "POST" else BookingSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        vehicle = serializer.validated_data["vehicle"]
        vehicle = vehicle.__class__.objects.select_for_update().get(pk=vehicle.pk)

        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]

        conflict = Booking.objects.filter(
            vehicle=vehicle,
            status__in=ACTIVE_STATUSES,
        ).filter(
            Q(start_date__lt=end_date) & Q(end_date__gt=start_date)
        ).exists()

        if conflict:
            raise serializers.ValidationError("Vehicle is already booked for this period.")

        days = (end_date - start_date).days
        serializer.save(
            renter=self.request.user,
            vehicle=vehicle,
            daily_price=vehicle.daily_price,
            total_price=days * vehicle.daily_price,
        )


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(renter=self.request.user).select_related("vehicle", "renter")


class ProviderBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(vehicle__provider__user=self.request.user).select_related("vehicle", "renter")


class ProviderBookingStatusView(generics.UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Booking.objects.filter(vehicle__provider__user=self.request.user).select_related("vehicle", "renter")

    def partial_update(self, request, *args, **kwargs):
        booking = self.get_object()
        new_status = request.data.get("status")
        allowed = {Booking.Status.APPROVED, Booking.Status.REJECTED}
        if new_status not in allowed:
            raise serializers.ValidationError({"status": "Status must be approved or rejected."})
        if booking.status != Booking.Status.PENDING:
            raise serializers.ValidationError("Only pending bookings can be updated.")
        booking.status = new_status
        booking.save(update_fields=["status", "updated_at"])
        return super().partial_update(request, *args, **kwargs)

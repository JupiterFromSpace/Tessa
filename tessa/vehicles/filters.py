import django_filters
from django.db import models
from django.db.models import Q
from bookings.models import Booking
from .models import Vehicle


class VehicleFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="daily_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="daily_price", lookup_expr="lte")
    available_from = django_filters.DateFilter(method="filter_availability")
    available_until = django_filters.DateFilter(method="filter_availability")

    class Meta:
        model = Vehicle
        fields = ["city", "category", "transmission", "fuel_type", "min_price", "max_price"]

    def filter_availability(self, queryset, name, value):
        start = self.data.get("available_from")
        end = self.data.get("available_until")
        if not start or not end:
            return queryset
        overlapping = Booking.objects.filter(
            vehicle=models.OuterRef("pk")
        ).filter(
            Q(start_date__lt=end) & Q(end_date__gt=start),
            status__in=[Booking.Status.PENDING, Booking.Status.APPROVED],
        )
        from django.db.models import Exists
        return queryset.annotate(has_overlap=Exists(overlapping)).filter(has_overlap=False)

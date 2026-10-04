from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "renter", "start_date", "end_date", "total_price", "status")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("vehicle__title", "renter__email")

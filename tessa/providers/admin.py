from django.contrib import admin
from .models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "verification_status", "created_at")
    list_filter = ("verification_status",)
    search_fields = ("user__email", "national_id", "driver_license_number")

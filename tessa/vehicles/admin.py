from django.contrib import admin
from .models import Vehicle, VehicleImage


class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 0


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("title", "provider", "city", "daily_price", "status")
    list_filter = ("status", "category", "transmission", "fuel_type", "city")
    search_fields = ("title", "brand", "model", "provider__user__email")
    inlines = [VehicleImageInline]


@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "created_at")

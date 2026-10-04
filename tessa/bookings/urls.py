from django.urls import path
from .views import BookingDetailView, BookingListCreateView, ProviderBookingListView, ProviderBookingStatusView

urlpatterns = [
    path("", BookingListCreateView.as_view(), name="booking-list-create"),
    path("<uuid:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("provider/", ProviderBookingListView.as_view(), name="provider-bookings"),
    path("provider/<uuid:pk>/status/", ProviderBookingStatusView.as_view(), name="provider-booking-status"),
]

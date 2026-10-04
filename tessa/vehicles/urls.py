from django.urls import path
from .views import VehicleDetailView, VehicleImageCreateView, VehicleListView, MyVehicleListCreateView

urlpatterns = [
    path("", VehicleListView.as_view(), name="vehicle-list"),
    path("mine/", MyVehicleListCreateView.as_view(), name="my-vehicles"),
    path("<uuid:pk>/", VehicleDetailView.as_view(), name="vehicle-detail"),
    path("<uuid:vehicle_id>/images/", VehicleImageCreateView.as_view(), name="vehicle-image-create"),
]

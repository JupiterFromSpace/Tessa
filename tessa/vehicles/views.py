from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from common.responses import success_response
from .filters import VehicleFilter
from .models import Vehicle, VehicleImage
from .serializers import VehicleImageCreateSerializer, VehicleSerializer


class VehicleListView(generics.ListAPIView):
    queryset = Vehicle.objects.filter(status=Vehicle.Status.ACTIVE).select_related("provider__user").prefetch_related("images")
    serializer_class = VehicleSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VehicleFilter
    search_fields = ["title", "brand", "model", "city"]
    ordering_fields = ["daily_price", "year", "created_at"]
    ordering = ["-created_at"]


class VehicleDetailView(generics.RetrieveAPIView):
    queryset = Vehicle.objects.filter(status=Vehicle.Status.ACTIVE).select_related("provider__user").prefetch_related("images")
    serializer_class = VehicleSerializer
    permission_classes = [AllowAny]


class MyVehicleListCreateView(generics.ListCreateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vehicle.objects.filter(provider__user=self.request.user).select_related("provider__user").prefetch_related("images")


class VehicleImageCreateView(generics.CreateAPIView):
    serializer_class = VehicleImageCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        vehicle = Vehicle.objects.get(id=self.kwargs["vehicle_id"], provider__user=self.request.user)
        serializer.save(vehicle=vehicle)

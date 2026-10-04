from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import ProviderProfile
from .serializers import ProviderProfileSerializer


class ProviderProfileCreateView(generics.CreateAPIView):
    serializer_class = ProviderProfileSerializer
    permission_classes = [IsAuthenticated]


class ProviderProfileMeView(generics.RetrieveAPIView):
    serializer_class = ProviderProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return ProviderProfile.objects.get(user=self.request.user)

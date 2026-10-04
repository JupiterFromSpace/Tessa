from django.urls import path
from .views import ProviderProfileCreateView, ProviderProfileMeView

urlpatterns = [
    path("profile/", ProviderProfileCreateView.as_view(), name="provider-profile-create"),
    path("profile/me/", ProviderProfileMeView.as_view(), name="provider-profile-me"),
]

from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    def validate(self, attrs):
        try:
            payload = id_token.verify_oauth2_token(
                attrs["id_token"], requests.Request(), settings.GOOGLE_CLIENT_ID
            )
        except ValueError as exc:
            raise serializers.ValidationError("Invalid Google ID token.") from exc

        if payload.get("email_verified") is not True:
            raise serializers.ValidationError("Google email is not verified.")

        email = payload.get("email")
        google_sub = payload.get("sub")
        if not email or not google_sub:
            raise serializers.ValidationError("Google account information is incomplete.")

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": payload.get("given_name", ""),
                "last_name": payload.get("family_name", ""),
                "google_sub": google_sub,
            },
        )

        if user.google_sub and user.google_sub != google_sub:
            raise serializers.ValidationError("This email is linked to another Google account.")

        if not user.google_sub:
            user.google_sub = google_sub
            user.first_name = payload.get("given_name", user.first_name)
            user.last_name = payload.get("family_name", user.last_name)
            user.save(update_fields=["google_sub", "first_name", "last_name"])

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }

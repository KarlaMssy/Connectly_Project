# auth_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import requests

User = get_user_model()

class GoogleLoginView(APIView):
    def post(self, request):
        google_token = request.data.get('token')

        if not google_token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the token with Google
        google_verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={google_token}"
        response = requests.get(google_verify_url)

        if response.status_code != 200:
            return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

        data = response.json()
        email = data.get('email')

        if not email:
            return Response({"error": "Google token did not return email"}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': email.split('@')[0]}
        )

        # Create or get auth token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "email": email,
                "username": user.username,
                "is_new_user": created
            }
        }, status=status.HTTP_200_OK)
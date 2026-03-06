from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class GoogleLoginView(APIView):
    def post(self, request):
        google_token = request.data.get('token')

        if not google_token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # MOCK VALIDATION
        email = f"user{google_token[-3:]}@gmail.com"

        user, created = User.objects.get_or_create(email=email, defaults={
            'username': email.split('@')[0],
        })

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "user": {"email": email}}, status=status.HTTP_200_OK)
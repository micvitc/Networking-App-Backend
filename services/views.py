#views.py
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from .serializers import UserRegistrationSerializer,MyTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import *



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Optional: You can send email verification here
            email_address=EmailAddress.objects.create(user=user, email=user.email, verified=False)
            send_email_confirmation(request, user, True)
            # Generate JWT tokens upon successful registration
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'user_data': serializer.data,  # Include user data in the response if needed
                    'email_verified': email_address.verified,  # Include email verification status
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YourProtectedAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]  # Optional
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Your view logic here
        pass

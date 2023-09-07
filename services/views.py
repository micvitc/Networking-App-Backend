#views.py
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.account.models import EmailAddress
from rest_framework.decorators import api_view
from allauth.account.utils import send_email_confirmation
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import generics
from .models import *
from django.shortcuts import get_object_or_404
from django.http import Http404

## Function Based Views
@api_view(['GET'])
def get_routes(request):
    routes = [
        '/register/',
        '/login/',
        '/logout/',
        '/verify/',
        '/token/refresh/',
        '/profile/create/',
        '/search/',
        '/profile/<slug:slug>/',
    ]
    return Response(routes)

class VerifyEmailStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            email_address = EmailAddress.objects.get(user=user, primary=True)
            email_verified = email_address.verified
            return Response({'email_verified': email_verified}, status=status.HTTP_200_OK)
        except EmailAddress.DoesNotExist:
            return Response({'email_verified': False}, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer

class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Unable to log out. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        
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


class ProfileSearchListView(generics.ListAPIView):
    serializer_class = ProfileSearchListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to include only profiles with non-null names
        queryset = Profile.objects.filter(name__isnull=False)

        # Exclude profiles with "Unverified" or "Blocked" profile types
        queryset = queryset.exclude(profile_type__in=["Unverified", "Blocked"])

        return queryset


class ProfileCreateView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer
    permission_classes = [IsAuthenticated]


class ProfileView(APIView):
    def get(self, request, slug):
        # Retrieve the profile object by slug
        profile = get_object_or_404(Profile, slug=slug)
        # Check if the profile is verified
        if profile.profile_type == "Unverified":
            raise Http404("Profile not found")  # Return a 404 error if the profile is unverified
        # Serialize the profile data

        serializer = ProfileViewSerializer(profile)

        return Response(serializer.data)
    
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

class PostRetrieveView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostViewSerializer
    lookup_field = 'slug'  # Use 'slug' as the lookup field for retrieving posts
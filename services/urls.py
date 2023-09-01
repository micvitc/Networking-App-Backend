# myapp/urls.py
from django.urls import path
from .views import UserRegistrationAPIView,MyTokenObtainPairView,VerifyEmailStatusView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('verify/',VerifyEmailStatusView.as_view(),name='verify-email'),
    # Add more endpoints as needed (e.g., login, logout, etc.)
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
]

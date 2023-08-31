# myapp/urls.py
from django.urls import path
from .views import UserRegistrationAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    # Add more endpoints as needed (e.g., login, logout, etc.)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token

]

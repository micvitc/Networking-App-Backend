# myapp/urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('',get_routes,name="get_routes"),

    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('verify/',VerifyEmailStatusView.as_view(),name='verify-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token

    path('profile/create/',ProfileCreateView.as_view(),name='profile-create'),
    path('search/', ProfileSearchListView.as_view(), name='user-profile-list'),
    path('profile/<slug:slug>/', ProfileView.as_view(), name='user-profile-detail'),
]

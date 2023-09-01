# serializers.py
import re
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from allauth.account.models import EmailAddress
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email']=user.email
        
        # Add custom claims to the token payload
        try:
            email_address = EmailAddress.objects.get(user=user, primary=True)
            token['email_verified'] = email_address.verified
        except EmailAddress.DoesNotExist:
            token['email_verified'] = False
        
        try:
            profile = Profile.objects.get(user=user)
            token['profile_data'] = {
                'name': profile.name,
                'profile_type': profile.profile_type,
                # Add other profile fields here
            }
        except Profile.DoesNotExist:
            token['profile_data'] = {}   
        return token
        

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        # Define a regular expression pattern to match the allowed email domains
        allowed_domains = r'@(vitstudent\.ac\.in|vit\.ac\.in)$'

        # Use the re module to match the email against the pattern
        if not re.search(allowed_domains, value):
            # If the email domain is not allowed, set profile_type to 'Unverified'
            self.initial_data['profile_type'] = 'Unverified'
        
        return value

    def validate(self, data):
        # Check if the username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        
        # Check if the email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        
        return data

    def create(self, validated_data):
        # Retrieve the profile_type from initial_data (set during email validation)
        profile_type = self.initial_data.get('profile_type', 'Student')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create a profile with the determined profile_type
        Profile.objects.create(user=user, profile_type=profile_type)
        
        return user

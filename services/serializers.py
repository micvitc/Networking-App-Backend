# serializers.py
import re
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from allauth.account.models import EmailAddress
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from taggit.models import Tag

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

    def validate(self, data):
        # Check if the username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        
        # Check if the email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user

class FollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    class Meta:
        model=Following
        fields=['following']
    def get_following(self,obj):
        return obj.following_id.name;

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']

class CommentSerializer(serializers.ModelSerializer):
    comment_profilename=serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['comments','date_commented','comment_profilename']
    def get_comment_profilename(self,obj):
        return obj.profile.name

class LikeSerializer(serializers.ModelSerializer):
    like_profilename=serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['like_profilename']
    def get_like_profilename(self,obj):
        return obj.profile.name

class PostSerializer(serializers.ModelSerializer):
    post_images=PostImageSerializer(many=True)
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    class Meta:
        model = Post
        fields = ['slug','caption','date_posted','post_images','likes','comments']

class ProfileViewSerializer(serializers.ModelSerializer):#to view induvidual profiles
    skills = TagSerializer(many=True)
    interests = TagSerializer(many=True)
    posts = PostSerializer(many=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('name', 'dept', 'admitted_year', 'profile_type', 'education_level', 'city','state',
                  'about', 'following', 'followers','profile_photo', 'privacy', 'skills', 'interests', 'linkedIn', 'instagram', 'posts')

    def get_following(self, obj):
        # Count the number of users you follow
        return Following.objects.filter(profile=obj).count()

    def get_followers(self, obj):
        # Count the number of users following you
        return Following.objects.filter(following_id=obj).count()

class ProfileSearchListSerializer(serializers.ModelSerializer):#to search for profiles
    class Meta:
        model = Profile
        fields = ('name', 'profile_photo', 'slug')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('department_name', 'program', 'department_school')

class ProfileSerializer(serializers.ModelSerializer):
    skills = TagSerializer(many=True)
    interests = TagSerializer(many=True)
    dept = DepartmentSerializer()  
    class Meta:
        model=Profile
        fields = '__all__'
    def create(self, validated_data):
        # Extract department data from validated data
        department_data = validated_data.pop('dept')
        # Extract skills and interests data
        skills_data = validated_data.pop('skills', [])
        interests_data = validated_data.pop('interests', [])

        # Create a new Department instance
        department, created = Department.objects.get_or_create(**department_data)
        # Create the Profile instance with the associated department
        profile = Profile.objects.create(dept=department, **validated_data)

        # Create skills and interests
        for skill_data in skills_data:
            Tag.objects.get_or_create(name=skill_data['name'])
            profile.skills.add(skill_data['name'])

        for interest_data in interests_data:
            Tag.objects.get_or_create(name=interest_data['name'])
            profile.interests.add(interest_data['name'])

        return profile

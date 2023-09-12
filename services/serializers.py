# serializers.py
import re
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from allauth.account.models import EmailAddress
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

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

class CommentSerializer(serializers.ModelSerializer):
    profilename=serializers.SerializerMethodField()
    profileslug=serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['comments','date_commented','profilename','profileslug']
    def get_profilename(self,obj):
        return obj.profile.name
    def get_profileslug(self,obj):
        return obj.profile.slug

class LikeSerializer(serializers.ModelSerializer):
    like_profilename=serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['like_profilename']
    def get_like_profilename(self,obj):
        return obj.profile.name

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']

class PostViewSerializer(serializers.ModelSerializer):
    post_images=PostImageSerializer(many=True)
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    class Meta:
        model = Post
        fields = ['caption','date_posted','post_images','likes','comments']

class PostCreateSerializer(serializers.ModelSerializer):
    post_images = PostImageSerializer(many=True, required=False)
    tags = TagListSerializerField() 

    class Meta:
        model = Post
        fields = ('caption', 'tags', 'post_images')

    def create(self, validated_data):
        post_images_data = validated_data.pop('post_images', [])
        tags_data = validated_data.pop('tags', [])
        
        # Automatically set the profile based on the authenticated user
        profile = self.context['request'].user.profile
        
        # Create the Post object
        post = Post.objects.create(profile=profile, **validated_data)
        post.tags.set(tags_data) 
        
        # Create PostImage instances and link them to the Post
        for image_data in post_images_data:
            PostImage.objects.create(post=post, **image_data)
        
        return post



class ProfilePostViewSerializer(serializers.ModelSerializer):
    post_images=PostImageSerializer(many=True)
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['slug','post_images','likes','comments']
    def get_likes(self,obj):
        return Like.objects.filter(post=obj).count()
    def get_comments(self,obj):
        return Comment.objects.filter(post=obj).count()

class ProfileViewSerializer(serializers.ModelSerializer):#to view induvidual profiles
    skills = TagListSerializerField()  # Use source to specify the related name
    posts = ProfilePostViewSerializer(many=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('name', 'dept', 'admitted_year', 'profile_type', 'education_level', 'city','state',
                  'about', 'following', 'followers','profile_photo', 'privacy', 'skills','linkedIn', 'instagram', 'posts')

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

class ProfileCreateSerializer(serializers.ModelSerializer):
    skills = TagListSerializerField()  # Use source to specify the related name
    dept = DepartmentSerializer()  
    class Meta:
        model=Profile
        fields = '__all__'
    def create(self, validated_data):
        department_data = validated_data.pop('dept')
        skills_data = validated_data.pop('skills', [])

        # Create or retrieve the department
        department, created = Department.objects.get_or_create(**department_data)

        # Create the profile
        profile = Profile.objects.create(dept=department, **validated_data)

        # Add skills to the profile
        profile.skills.set(skills_data)  # Set the skills for the profile
        return profile


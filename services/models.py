import uuid
import shortuuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .choices import *
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.utils.text import slugify


# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length = 100,null=True)
    program = models.CharField(max_length = 100,null=True)
    department_school = models.CharField(max_length = 100,choices = SCHOOL_CHOICES,null=True)
    
    def __str__(self):
        return str(self.department_name)+' -> '+str(self.program)+' -> '+str(self.department_school)

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True)
    dept=models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    admitted_year=models.CharField(max_length=200,blank=True, null=True)
    profile_type=models.CharField(max_length=100, choices=STATUS_CHOICES, default="Unverified")
    education_level=models.CharField(max_length=100,blank=True, null=True)
    about=models.TextField(null=True)
    profile_photo=models.URLField(max_length=200,blank=True, null=True)
    privacy=models.CharField(max_length=100, choices=PRIVACY_CHOICES, default="Public")
    
    city=models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null = True)

    phone_number = PhoneNumberField( null=True)
    linkedIn = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)

    skills = TaggableManager(blank=True)

    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super(Profile, self).save(*args, **kwargs)
    def __str__(self):
        return self.user.username
    

class Feedback(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    feedback = models.TextField()
    
    def __str__(self):
        return f"Feedback id ({self.id}) --> {self.profile.user.username}"


class Following(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profile_p')
    following_id = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='following_profile')
    date_followed = models.DateField(auto_now_add=True)
    request_status = models.CharField(max_length=100, choices=REQUEST_STATUS,default="Followed")
    slug = models.SlugField(blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = shortuuid.ShortUUID().random(length=10)
        super(Following, self).save(*args, **kwargs)
    def __str__(self):
        if self.request_status=="Pending":
            return str(self.profile.user.username) + " wants to follow " + str(self.following_id.user.username)
        else:
            return str(self.profile.user.username) + " is following " + str(self.following_id.user.username)


class Post(models.Model):
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    caption=models.CharField(max_length=250)
    tags=TaggableManager(blank=True)
    date_posted=models.DateField(auto_now_add=True)
    slug = models.SlugField(blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = shortuuid.ShortUUID().random(length=10)
        super(Post, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.profile.user.username)+" --> post_id ("+str(self.pk)+") --> ("+str(self.date_posted)+")"

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    image = models.URLField(max_length=200)
    slug = models.SlugField(blank=True)
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = shortuuid.ShortUUID().random(length=10)
        super(PostImage, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.post.profile.user.username)+" --> post_id ("+str(self.post.slug)+") --> image_id ("+str(self.slug)+")"

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    comments=models.TextField()
    date_commented=models.DateField(auto_now_add=True)
    slug = models.SlugField(blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = shortuuid.ShortUUID().random(length=10)
        super(Comment, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.profile.user.username)+" commented on "+str(self.post.profile.user.username)+ "'s post"

class Like(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = shortuuid.ShortUUID().random(length=10)
        super(Like, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.profile.user.username)+" liked "+str(self.post.profile.user.username)+ "'s post"



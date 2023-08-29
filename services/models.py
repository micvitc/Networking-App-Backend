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

class SkillTag(TaggedItemBase):
    content_object = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="skill_tag")

class InterestTag(TaggedItemBase):
    content_object = models.ForeignKey("Profile", on_delete=models.CASCADE,related_name="interest_tag")

class HashTag(TaggedItemBase):
    content_object = models.ForeignKey("Post", on_delete=models.CASCADE,related_name="hash_tag")


# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length = 100)
    program = models.CharField(max_length = 100)
    department_school = models.CharField(max_length = 100,choices = SCHOOL_CHOICES)
    
    def __str__(self):
        return str(self.department_name)+' -> '+str(self.program)+' -> '+str(self.department_school)

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    dept=models.ForeignKey(Department, on_delete=models.CASCADE)
    admitted_year=models.CharField(max_length=200,null=True)
    status=models.CharField(max_length=100, choices=STATUS_CHOICES, default="Current")
    education_level=models.CharField(max_length=100)
    about=models.TextField()
    profile_photo=models.URLField(max_length=200)
    
    privacy=models.CharField(max_length=100, choices=PRIVACY_CHOICES, default="Public")

    phone_number = PhoneNumberField(blank=True, null=True)
    linkedIn = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)

    skills = TaggableManager(through=SkillTag,related_name="skill_tag")
    interests = TaggableManager(through=InterestTag,related_name="interest_tag")

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
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profile')
    following_id = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='following_profile')
    date_followed = models.DateField(auto_now_add=True)
    request_status = models.CharField(max_length=100, choices=REQUEST_STATUS,default="Pending")
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
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption=models.CharField(max_length=250)
    tags=TaggableManager(through=HashTag,related_name="hash_tag")
    image_or_video=models.URLField(max_length=200)
    date_posted=models.DateField(auto_now_add=True)
    slug = models.SlugField(blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = shortuuid.ShortUUID().random(length=10)
        super(Post, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.profile.user.username)+" --> post_id ("+str(self.pk)+") --> ("+str(self.date_posted)+")"

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
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
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = shortuuid.ShortUUID().random(length=10)
        super(Like, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.profile.user.username)+" liked "+str(self.post.profile.user.username)+ "'s post"



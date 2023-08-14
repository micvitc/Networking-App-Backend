from django.db import models

Status_Choices = [("AL","Alumini"), ("CR","Current"),("FA","Faculty")]
privacy_Choices = [("PU","Public"),("PR","Private")]
Request_Status_Choices=[("PE","Pending"),("AC","Accepted")]

class Profile(models.Model):
    Name=models.CharField(max_length=100)
    userid=models.CharField(max_length=100, primary_key=True, unique=True)
    deptid=models.ForeignKey("department", on_delete=models.CASCADE)
    year_of_joining=models.EmailField(max_length=254)
    status=models.CharField(max_length=100, choices=Status_Choices, default="CR")
    education_level=models.CharField(max_length=10)
    about=models.TextField()
    profile_photo=models.URLField(max_length=200)
    privacy=models.CharField(max_length=100, choices=privacy_Choices, default="PU")
    phone_number=models.PositiveBigIntegerField()
    linkedIn=models.URLField(max_length=200)
    instagram=models.URLField(max_length=200)
    skills=models.TextField()
    interests=models.TextField()

class department(models.Model):
    deptid=models.CharField(max_length=100, primary_key=True, unique=True)
    dept_name=models.CharField(max_length=100)
    program=models.CharField(max_length=100)
    School=models.CharField(max_length=100)

class Feedback(models.Model):
    userid=models.ForeignKey(Profile, on_delete=models.CASCADE)
    feedback=models.TextField()

class Following(models.Model):
    userid=models.ForeignKey(Profile, on_delete=models.CASCADE)
    followingid=models.CharField(max_length=100, primary_key=True)
    date_followed=models.DateField()
    request_status=models.CharField(max_length=100, choices=Request_Status_Choices)

class Posts(models.Model):
    postid=models.CharField(max_length=100, primary_key=True, unique=True)
    userid=models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption=models.CharField(max_length=250)
    tags=models.CharField(max_length=250)
    image_or_video=models.URLField(max_length=200)

class Comments(models.Model):
    postid=models.ForeignKey(Posts, on_delete=models.CASCADE)
    userid=models.ForeignKey(Profile, on_delete=models.CASCADE)
    comments=models.TextField()

class Likes(models.Model):
    postid=models.ForeignKey(Posts, on_delete=models.CASCADE)
    userid=models.ForeignKey(Profile, on_delete=models.CASCADE)

class Users(models.Model):
    profile=models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=100)





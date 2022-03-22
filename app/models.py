from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

ROLE = [
        ('Admin', 'Admin'),
        ('Writer', 'Writer'),
        ('Editor', 'Editor'),
        ('Publisher', 'Publisher'),
        ('Approver', 'Approver')
    ]

from django.contrib.auth.models import AbstractUser

class UserCustom(AbstractUser):
    role = models.CharField(choices=ROLE,max_length=20,null=True,blank=True)
    accessint = models.IntegerField(validators=[
        MaxValueValidator(limit_value=7),
        MinValueValidator(limit_value=1)
    ],null=True,blank=True)

# class userdata(models.Model):
#     user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
#     role = models.CharField(choices=ROLE,max_length=20,null=True,blank=True)
#     accessint = models.IntegerField(validators=[
#         MaxValueValidator(limit_value=7),
#         MinValueValidator(limit_value=1)
#     ],null=True,blank=True)

class apwire_ContentPitching(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()
    # permissions = models.CharField(max_length=20) 

class apwire_WritingRewrite(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

class apwire_ReviewDraft1(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()
    
class apwire_ReviewDraft2(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

class apwire_FDNApproval(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

class apwire_ReadyForRelease(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

class apwire_APPublished(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

# //////////////////////////////////////////////////

class apnews_ContentPitching(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

class apnews_WritingRewrite(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

class apnews_ReviewDraft1(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()
    
class apnews_ReviewDraft2(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

class apews_FDNApproval(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

class apnews_ReadyForRelease(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()

class apnews_APPublished(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    Date = models.DateField()
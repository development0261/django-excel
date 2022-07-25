from datetime import date
from email.mime import image
from unittest.util import _MAX_LENGTH

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import admin
ROLE = [
        ('Admin', 'Admin'),
        ('Writer', 'Writer'),
        ('Editor', 'Editor'),
        ('Publisher', 'Publisher'),
        ('Approver', 'Approver')
    ]

STAT = [
        ('Draft', 'Draft'),
        ('In progress', 'In progress'),
        ('Completed', 'Completed'),
    ]

tables_choice = [
    ('Content_Pitching','Story Pitching'),
    ('Writing_Rewrite','Writing & Rewriting'),
    ('Review_Draft_1','First Review'),
    ('Review_Draft_2','Second Review'),
    ('FDN_Approval_1','Ready For FDN Approval'),
    ('Ready_For_Release','Ready For Release'),
    ('App_Published','AP Published')
]

from django.contrib.auth.models import AbstractUser

class UserCustom(AbstractUser):
    accessint = models.IntegerField(default=7,validators=[
        MaxValueValidator(limit_value=7),
        MinValueValidator(limit_value=1)
    ],null=True,blank=True)

    # If flag false then account works for ap.shakticoin
    AP_flag = models.BooleanField(default=False)

    def get_table_role(self):
        return {
            'Content_Pitching':self.Content_Pitching,
            'Writing_Rewrite':self.Writing_Rewrite,
            'Review_Draft_1':self.ReviewDraft1,
            'Review_Draft_2':self.ReviewDraft2,
            'FDN_Approval_1':self.FDNApproval,
            'Ready_For_Release':self.ReadyForRelease,
            'App_Published':self.APPublished
        }
    
from ckeditor.fields import RichTextField
import uuid


class content_brief(models.Model):
    topic = models.CharField(max_length=100)
    description = RichTextField()
    class Meta:
      verbose_name_plural = "Content Brief"

class category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
      verbose_name_plural = "Category"


class Ap_Wire(models.Model):
    topic = models.CharField(max_length=200)
    author = models.ForeignKey(UserCustom,on_delete=models.CASCADE)
    description = RichTextField()
    image = models.ImageField(upload_to='media/',null=True,blank=True) 
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=tables_choice,max_length=30,default="APWire_Content_Pitching")
    published_on = models.DateTimeField(null=True, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateTimeField(auto_now=True)
    reverted_count = models.IntegerField(default=1)
    category = models.ForeignKey(category,null=True,blank=True ,on_delete=models.CASCADE)
    # blog_release_status = models.ForeignKey(blog_progress_status,on_delete=models.CASCADE)
    blog_release_status = models.CharField(max_length=30,choices=STAT,default="In progress")
    downloadstatus = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "AP-Wire"

class moreimages_apwire(models.Model):
    post = models.ForeignKey(Ap_Wire, default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/',verbose_name='Image')

    class Meta:
        verbose_name_plural = "AP-Wire Images"

class Ap_News(models.Model):
    topic = models.CharField(max_length=200)
    author = models.ForeignKey(UserCustom,on_delete=models.CASCADE)
    description = RichTextField()
    image = models.ImageField(upload_to='media/',null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=tables_choice,max_length=30,default="APNews_Content_Pitching")
    published_on = models.DateTimeField (null=True, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateTimeField(auto_now=True)
    reverted_count = models.IntegerField(default=1)
    category = models.ForeignKey(category,null=True,blank=True ,on_delete=models.CASCADE)
    blog_release_status = models.CharField(max_length=30,choices=STAT,default="In progress")
    # blog_release_status = models.ForeignKey(blog_progress_status,on_delete=models.CASCADE)
    downloadstatus = models.BooleanField(default=False)

    class Meta:
      verbose_name_plural = "AP-News"

class moreimages_apnews(models.Model):
    post = models.ForeignKey(Ap_News, default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/',verbose_name='Image')

    class Meta:
        verbose_name_plural = "AP-News Images"


class permissions(models.Model):
    user = models.ManyToManyField(UserCustom)
    status = models.CharField(choices=tables_choice,max_length=20,unique=True)
    create = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
    view = models.BooleanField(default=False)
    move = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    to_delete = models.BooleanField(default=False,verbose_name="delete")
    Permission_Name = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
      verbose_name_plural = "Permissions"

        
class Mangeimages(models.Model):
    image = models.ImageField(upload_to='media/')

    class Meta:
      verbose_name_plural = "manage image"

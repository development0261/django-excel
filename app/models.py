from datetime import date
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
    

    # def get_role_data(self):
    #     return UserTableConnection.objects.filter(user = self)
# class userdata(models.Model):
#     user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
#     role = models.CharField(choices=ROLE,max_length=20,null=True,blank=True)
#     accessint = models.IntegerField(validators=[
#         MaxValueValidator(limit_value=7),
#         MinValueValidator(limit_value=1)
#     ],null=True,blank=True)

from ckeditor.fields import RichTextField
import uuid

# categories = {
#     ('Education','Education'),
#     ("Minig Digital Currency","Minig Digital Currency"),
#     ("MSB & PayDay","MSB & PayDay"),
#     ("Child Poverty","Child Poverty"),
#     ("Money with Hearts and Mind","Money with Hearts and Mind")
# }



class content_brief(models.Model):
    topic = models.CharField(max_length=100)
    description = RichTextField()
    class Meta:
      verbose_name_plural = "Content Brief"

class category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
      verbose_name_plural = "Category"

# class blog_progress_status(models.Model):
#     name = models.CharField(choices=STAT,max_length=100,default="In progress")
#     class Meta:
#       verbose_name_plural = "Status"


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



    
        
        


# class apwire_ContentPitching(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()
#     # permissions = models.CharField(max_length=20)

# class apwire_WritingRewrite(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# class apwire_ReviewDraft1(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()
    
# class apwire_ReviewDraft2(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# class apwire_FDNApproval(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# class apwire_ReadyForRelease(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# class apwire_APPublished(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# # //////////////////////////////////////////////////

# class apnews_ContentPitching(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# class apnews_WritingRewrite(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# class apnews_ReviewDraft1(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()
    
# class apnews_ReviewDraft2(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# class apews_FDNApproval(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# class apnews_ReadyForRelease(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()

# class apnews_APPublished(models.Model):
#     title = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     Date = models.DateField()



# class UserTableConnection(models.Model):
#     user = models.ForeignKey(UserCustom,on_delete=models.CASCADE)
#     role = models.CharField(choices=ROLE,max_length=20,null=True,blank=True)
#     tables = MultiSelectField(choices=tables_choice)
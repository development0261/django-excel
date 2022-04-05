from datetime import date
from secrets import choice
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

tables_choice = [
    ('Content_Pitching','Content_Pitching'),
    ('Writing_Rewrite','Writing_Rewrite'),
    ('Review_Draft_1','Review_Draft_1'),
    ('Review_Draft_2','Review_Draft_2'),
    ('FDN_Approval_1','FDN_Approval_1'),
    ('Ready_For_Release','Ready_For_Release'),
    ('App_Published','App_Published')
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


class Ap_Wire(models.Model):
    topic = models.CharField(max_length=30)
    author = models.ForeignKey(UserCustom,on_delete=models.CASCADE)
    description = RichTextField()
    image = models.ImageField(null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=tables_choice,max_length=30,default="APWire_Content_Pitching")
    publishedon = models.DateField(null=True, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateField(auto_now=True)

    class Meta:
      verbose_name_plural = "Ap-Wire"

class Ap_News(models.Model):
    topic = models.CharField(max_length=30)
    author = models.ForeignKey(UserCustom,on_delete=models.CASCADE)
    description = RichTextField()
    image = models.ImageField(null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=tables_choice,max_length=30,default="APNews_Content_Pitching")
    publishedon = models.DateField(null=True, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateField(auto_now=True)

    class Meta:
      verbose_name_plural = "Ap-News"



class permissions(models.Model):
    user = models.ManyToManyField(UserCustom)
    status = models.CharField(choices=tables_choice,max_length=20)
    create = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
    view = models.BooleanField(default=False)
    move = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    to_delete = models.BooleanField(default=False,verbose_name="delete")
    Permission_Name = models.CharField(max_length=20,null=True,blank=True)

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
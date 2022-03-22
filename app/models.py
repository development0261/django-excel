from datetime import date
from secrets import choice
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField
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
    Content_Pitching = models.CharField(choices=ROLE, max_length=20,default="Writer")
    Writing_Rewrite = models.CharField(choices=ROLE, max_length=20,default="Writer")
    ReviewDraft1 = models.CharField(choices=ROLE, max_length=20,default="Writer")
    ReviewDraft2 = models.CharField(choices=ROLE, max_length=20,default="Writer")
    FDNApproval = models.CharField(choices=ROLE, max_length=20,default="Writer")
    ReadyForRelease = models.CharField(choices=ROLE, max_length=20,default="Writer")
    APPublished = models.CharField(choices=ROLE, max_length=20,default="Writer")
    accessint = models.IntegerField(validators=[
        MaxValueValidator(limit_value=7),
        MinValueValidator(limit_value=1)
    ],null=True,blank=True)

    # def get_role_data(self):
    #     return UserTableConnection.objects.filter(user = self)
# class userdata(models.Model):
#     user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
#     role = models.CharField(choices=ROLE,max_length=20,null=True,blank=True)
#     accessint = models.IntegerField(validators=[
#         MaxValueValidator(limit_value=7),
#         MinValueValidator(limit_value=1)
#     ],null=True,blank=True)

class Blog(models.Model):
    topic = models.CharField(max_length=30)
    author = models.ForeignKey(UserCustom,on_delete=models.CASCADE)
    description = models.TextField(max_length=300)
    image = models.ImageField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=tables_choice,max_length=30,default="APWire_Content_Pitching")
    

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
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    options = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others','Others')
    )
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile_data')
    gender = models.CharField(
        max_length = 20,
        choices = options,
        default = 'male',
        null=False,
        blank=False
        )
    dob=models.DateField(null=True,blank=True,default=None)
    phone=models.CharField(max_length=20,null=True,blank=True)
    works_at=models.CharField(max_length=200,null=True,blank=True)
    lives_in=models.CharField(max_length=200,null=True,blank=True)
    studies_at=models.CharField(max_length=200,null=True,blank=True)
    profile_image=models.ImageField(upload_to="profile_image",null=True,blank=True)

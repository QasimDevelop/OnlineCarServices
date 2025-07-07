from pickle import FALSE
import profile
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    CHOICES=(("user","user"),
    ("stations","stations"),
    ("admin","admin"))
    role=models.CharField(max_length=10,choices=CHOICES,default="user")
    phone=models.CharField(max_length=10,null=True,blank=True)
    profile_picture=models.ImageField(upload_to="profile_pictures",null=True,blank=True)

    def __str__(self):
        return self.username

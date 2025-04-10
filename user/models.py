from django.db import models
import PIL
class User(models.Model):
    status_choices = [
        ('admin','Admin'),
        ('user','User'),
    ]
    username = models.CharField(max_length=200,null=True, blank=True,unique=True)
    email = models.CharField(max_length=200, unique=True,null=True, blank=True)
    password = models.CharField(max_length=400,null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=15)
    first_name = models.CharField(max_length=50, default='',null=True, blank=True)
    last_name = models.CharField(max_length=50, default='',null=True, blank=True)
    date_of_birth = models.DateField(default=None,null=True, blank=True)
    nick = models.CharField(max_length=100, default="Snack King", null=True, blank=True); 
    profilePicture = models.ImageField(upload_to='images/',null=True, blank=True)
    role = models.CharField(max_length=20, default='user', null=True,blank=True,choices=status_choices)
    cover_photo = models.ImageField(upload_to='cover_photos/', null=True, blank=True)
    is_logged_in = models.BooleanField(default=False,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.email

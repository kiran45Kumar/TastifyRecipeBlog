from django.db import models
import PIL
class User(models.Model):
    username = models.CharField(max_length=200,null=True, blank=True,unique=True)
    email = models.CharField(max_length=200, unique=True,null=True, blank=True)
    password = models.CharField(max_length=400,null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=50, default='',null=True, blank=True)
    last_name = models.CharField(max_length=50, default='',null=True, blank=True)
    date_of_birth = models.DateField(default=None,null=True, blank=True)
    nick = models.CharField(max_length=10, default="Snack King", null=True, blank=True); 
    profilePicture = models.ImageField(upload_to='images/',null=True, blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', null=True, blank=True)
    is_logged_in = models.BooleanField(default=False,null=True, blank=True)
    def __str__(self) -> str:
        return self.email

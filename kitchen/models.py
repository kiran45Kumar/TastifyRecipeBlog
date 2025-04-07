from django.db import models
from user.models import User
# Create your models here.
class Kitchen(models.Model):
    kitchen_id = models.AutoField(primary_key=True)
    kitchen_name = models.CharField(max_length=80, null=False, blank=False,unique=True)#required
    kitchen_desc = models.TextField(max_length=80, null=False, blank=False)#required
    website_url = models.URLField(unique=True, blank=True, null=True) #optional
    business_email = models.EmailField(unique=True, null=True,blank=True) #optional
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) #required
    kitchen_logo = models.ImageField(upload_to='kitchen_logo/',null=True, blank=True) #required
    kitchen_images = models.FileField(upload_to='kitchen_images/',null=True, blank=True) #optional
    kitchen_videos = models.FileField(upload_to='kitchen_videos/',null=True, blank=True) #optional 
    location = models.TextField() #required
    rating = models.IntegerField(null=True, blank=True) #will be given by user;
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
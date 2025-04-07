from django.db import models
from user.models import User
# Create your models here.
class CookingCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=25, null=True, blank=True)
    sub_category = models.ForeignKey('self',on_delete=models.SET_NULL,null=True, blank=True,related_name='sub_categories')
class Kitchen(models.Model):
    kitchen_id = models.AutoField(primary_key=True)
    kitchen_name = models.CharField(max_length=80, null=False, blank=False,unique=True) #required
    kitchen_desc = models.TextField(max_length=80, null=False, blank=False) #required
    website_url = models.URLField(unique=True, blank=True, null=True) #optional
    business_email = models.EmailField(unique=True, null=True,blank=True) #optional
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) #required
    kitchen_logo = models.ImageField(upload_to='kitchen_logo/',null=True, blank=True) #required
    kitchen_images = models.FileField(upload_to='kitchen_images/',null=True, blank=True) #optional
    kitchen_videos = models.FileField(upload_to='kitchen_videos/',null=True, blank=True) #optional 
    location = models.TextField() #required
    cooking_category = models.ForeignKey(CookingCategory, on_delete=models.CASCADE, null=True, blank=True)#optional
    rating = models.IntegerField(null=True, blank=True) #will be given by user;
    createdAt = models.DateTimeField(auto_now_add=True) #auto
    updatedAt = models.DateTimeField(auto_now=True) #auto
    
    def __str__(self):
        return self.kitchen_name
    
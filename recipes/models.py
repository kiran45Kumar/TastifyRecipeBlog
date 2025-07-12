from django.db import models
from user.models import User
from kitchen.models import Kitchen
# Create your models here.
class RecipeCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=25, null=True, blank=True)
    sub_category = models.ForeignKey('self',on_delete=models.SET_NULL,null=True, blank=True,related_name='sub_categories')

class Recipes(models.Model):
    status_choices = [
        ('pending','Pending'),
        ('draft','Draft'),
        ('published','Published'),
    ]
    reciepe_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_title = models.CharField(max_length=50,default='')
    description = models.TextField(max_length=500,default='')
    ingredients = models.CharField(max_length=1500,default='')
    instructions = models.CharField(max_length=1500,default='')
    prep_time = models.CharField(max_length=60,default='')
    category = models.ForeignKey(RecipeCategory,on_delete=models.CASCADE, null=True, blank=True)
    cook_time = models.CharField(max_length=30,default='') 
    # kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, null=True,blank=True)
    # tags = models.JSONField(default=list,null=True, blank=True)
    status = models.CharField(max_length=30, default="Pending",choices=status_choices)
    serving_size = models.CharField(max_length=30,default='') 
    likes = models.IntegerField(default=0, null=True, blank=True)
    views = models.IntegerField(default=0, null=True, blank=True)
    post_url = models.FileField(upload_to='uploads/')
    nutrition_info = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# for django shell __str__() is used
    def __str__(self) :
        return f'{self.reciepe_id} - {self.recipe_title,} - {self.user_id}'
    def increment_views(self):
        """Increment the view count for the recipe."""
        self.views += 1
        self.save(update_fields=['views'])

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'recipe') 

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self) :
        return f'Comment By {self.comment_id} - {self.content,} - {self.parent}'

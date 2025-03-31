from django.db import models
from user.models import User
# Create your models here.
class Recipes(models.Model):
    reciepe_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_title = models.CharField(max_length=40,default='')
    description = models.TextField(max_length=500,default='')
    ingredients = models.CharField(max_length=200,default='')
    instructions = models.CharField(max_length=200,default='')
    prep_time = models.CharField(max_length=200,default='')
    cook_time = models.CharField(max_length=200,default='') 
    serving_size = models.CharField(max_length=200,default='') 
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
    comments = models.CharField(max_length=5000, default='')
    reply = models.CharField(max_length=5000, default='')
    # for django shell __str__() is used
    def __str__(self) :
        return f'{self.comment_id} - {self.comments,} - {self.reply}'

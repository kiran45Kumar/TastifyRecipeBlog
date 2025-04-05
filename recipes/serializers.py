from rest_framework import serializers
from .models import Comments, Recipes

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['comment_id', 'recipe_id', 'user_id', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']
class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = "__all__"
        read_only_fields = ['reciepe_id', 'created_at']
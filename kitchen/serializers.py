from rest_framework import serializers
from kitchen.models import Kitchen, CookingCategory

class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = '__all__'
class CookingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingCategory
        fields = '__all__'
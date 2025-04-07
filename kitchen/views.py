from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from kitchen.models import Kitchen, CookingCategory
from kitchen.serializers import KitchenSerializer, CookingCategorySerializer
# Create your views here.

class KitchenViewSet(ModelViewSet):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer

class CookingCategoryViewSet(ModelViewSet):
    queryset = CookingCategory.objects.all()
    serializer_class = CookingCategorySerializer

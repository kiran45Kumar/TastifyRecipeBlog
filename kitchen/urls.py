from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kitchen.views import *
router = DefaultRouter()
router.register(r'kitchens',KitchenViewSet, basename='kitchen')
router.register(r'categories',CookingCategoryViewSet, basename='categories')
url_patterns = [
    path('api/', include(router.urls))
    # template views
]
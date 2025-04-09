from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kitchen.views import *
router = DefaultRouter()
router.register(r'kitchens',KitchenViewSet, basename='kitchen')
router.register(r'categories',CookingCategoryViewSet, basename='categories')
urlpatterns = [
    path('api/', include(router.urls)),
    # template views
    path('create_kitchen/',CreateKitchen.as_view(), name='create_kitchen'),
    path('add_kitchen/',AddKitchen.as_view(), name='AddKitchen'),
    path('upload_image_video/',CreateImageVideo.as_view(), name='CreateImageVideo'),
    path('kitchen_dashboard/<int:id>',kitchen_dashboard, name='kitchen_dashboard'),
    path('recipes/<int:id>',recipes, name='recipes'),
    path('view_recipes/<int:id>',view_recipes, name='recipes'),
    path('kitchen_profile/<int:id>',kitchen_profile, name='recipes'),
    path('update_recipe/<int:id>/<int:rid>',update_recipe, name='update_recipe'),
    # path('create_recipe/<int:id>',create_recipe, name='create_recipe'),
]
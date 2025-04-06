from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'recipes', RecipesViewSet,basename='recipes')
urlpatterns = [
    path('user/<str:name>/<int:id>/posts',ViewUser.as_view(),name='view_posts'),
    path('create_post/',RecipePosts.as_view(), name='create_post'),
    path('update_recipes/',UpdateRecipe.as_view(), name='update_recipe'),
    path('api/',include(router.urls)),
    path('like/',LikePost.as_view(), name='like_post'),
    path('send_request/', SendRequest.as_view(), name='send_request'),
    path('delete_comment/', DeleteComment.as_view(), name='DeleteComment'),
    path('change_draft/', Draft.as_view(), name='change_draft'),
]
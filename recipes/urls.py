from django.urls import path
from .views import *
urlpatterns = [
    path('user/<str:name>/<int:id>/posts',ViewUser.as_view(),name='view_posts'),
    path('create_post/',RecipePosts.as_view(), name='create_post'),
    path('delete_post/',DeletePost.as_view(), name='delete_post'),
    path('like/',LikePost.as_view(), name='like_post'),
    path('send_request/', SendRequest.as_view(), name='send_request'),
    path('delete_comment/', DeleteComment.as_view(), name='DeleteComment'),
    path('change_draft/', Draft.as_view(), name='change_draft'),
]
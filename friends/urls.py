from django.urls import path
from .views import *
urlpatterns = [
    path('SendRequest/', SendFriendRequest.as_view(), name='send_friend_request'),
]
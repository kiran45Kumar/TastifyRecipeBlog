from django.db import models
from user.models import User
class MyFriends(models.Model):
    id = models.AutoField(primary_key=True)
    current_user = models.CharField(max_length=10,default='')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    
    def __str__(self):
        return f'{self.current_user} - {self.friend.username}'
class FriendRequest(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=100, default='New Friend Request', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True,related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='reciever')
    status = models.CharField(max_length=12, choices=status_choices, default='pending')
    createdAt = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'From user {self.sender.username} - {self.reciever.username}'
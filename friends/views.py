from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from friends.models import FriendRequest
from user.models import User
class SendFriendRequest(APIView):
    def post(self, request):
        sender_id = request.session.get('user_id', None)
        receiver_id = request.POST.get('userId')
        try:
            receiver = User.objects.get(id=receiver_id)
            if sender_id == receiver.id:
                return JsonResponse({"status": "fail", "message": "You cannot send a friend request to yourself."}, status=400)
            
            sender = User.objects.get(id=sender_id)
            friend_request, created = FriendRequest.objects.get_or_create(sender=sender, reciever=receiver)

            if created:
                return JsonResponse({'status': 'pass', 'message': 'Friend request sent successfully'}, status=200)
            else:
                return JsonResponse({'status': 'fail', 'message': 'Friend request already sent'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "User not found."}, status=404)
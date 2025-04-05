from typing import Any
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q, Prefetch
from friends.models import FriendRequest
from .models import  Like, Recipes, Comments
from rest_framework.views import APIView
from django.http import JsonResponse
from user.models import User
from django.views.generic.base import TemplateView
from rest_framework import viewsets
from recipes.serializers import CommentsSerializer
# Create your views here.
class RecipePosts(APIView):
    def post(self, request):
        title = request.data.get('title')
        desc = request.data.get('desc')
        ingredients = request.data.get('ingredients')
        instruction = request.data.get('instruction')
        preptime = request.data.get('preptime')
        cooktime = request.data.get('cooktime')
        servSize = request.data.get('servSize')
        nutrition = request.data.get('nutrition')
        userId = request.data.get('userId')
        postimg = request.FILES.get('postimg')
        user = get_object_or_404(User, id = userId)
        recipe = Recipes()
        recipe.user_id = user
        recipe.recipe_title = title
        recipe.description = desc 
        recipe.ingredients = ingredients
        recipe.instructions = instruction
        recipe.prep_time = preptime
        recipe.cook_time = cooktime
        recipe.status = 'Published'
        recipe.serving_size = servSize
        recipe.nutrition_info = nutrition
        recipe.post_url = postimg
        recipe.save()
        return JsonResponse({"status":"pass"})
class Draft(APIView):
    def post(self, request):
        title = request.data.get('title')
        desc = request.data.get('desc')
        ingredients = request.data.get('ingredients')
        instruction = request.data.get('instruction')
        preptime = request.data.get('preptime')
        cooktime = request.data.get('cooktime')
        servSize = request.data.get('servSize')
        nutrition = request.data.get('nutrition')
        userId = request.data.get('userId')
        postimg = request.FILES.get('postimg')
        user = get_object_or_404(User, id = userId)
        recipe = Recipes()
        recipe.user_id = user
        recipe.recipe_title = title
        recipe.description = desc 
        recipe.ingredients = ingredients
        recipe.instructions = instruction
        recipe.prep_time = preptime
        recipe.cook_time = cooktime
        recipe.status = 'Draft'
        recipe.serving_size = servSize
        recipe.nutrition_info = nutrition
        recipe.post_url = postimg
        recipe.save()
        return JsonResponse({"status":"pass"})
def posts(request):
    rposts = Recipes.objects.all()
    return render(request, 'user/userdasboard.html',{'rposts':rposts})
class ViewUser(TemplateView):
    template_name = 'user/baseposts.html'
    def get(self, request, *args, **kwargs):
        uid = request.session.get('user_id', None)
        if not uid:
            error = "You are not logged in"
            return redirect('404', message=error)
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uid = self.request.session.get('user_id', None)
        reciepes = Recipes.objects.filter(user_id=uid)
        user = User.objects.filter(id=uid)
        self.request.session['post_count'] = reciepes.count()
        user_u = User.objects.get(id=uid)

        # Friends and requests
        pending_requests = FriendRequest.objects.filter(reciever=user_u, status__iexact='pending')
        accepted_requests = FriendRequest.objects.filter(
            (Q(reciever=user_u) | Q(sender=user_u)), status__iexact='accepted'
        )
        friends = set()
        for request in accepted_requests:
            if request.sender != user_u:
                friends.add(request.sender)
            if request.reciever != user_u:
                friends.add(request.reciever)

        # Prefetch comments and replies for all posts
        top_level_comments = Comments.objects.filter(parent__isnull=True).select_related('user_id')
        allposts = Recipes.objects.filter(status = 'Published').prefetch_related(
            Prefetch('comments_set', queryset=top_level_comments.prefetch_related('replies'))
        ).order_by('-created_at')

        context.update({
            "allposts": allposts,
            'currentUser': self.request.session.get('user_name'),
            'postCount': self.request.session.get('post_count'),
            'users': user,
            "current_user_id": uid,
            'nick_name': self.request.session.get('user_nick_name'),
            'friends': friends,
            'pending_requests': pending_requests,
        })
        return context
class DeletePost(APIView):
    def delete(self, request):
        id = request.data.get('id') 
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            recipe = Recipes.objects.get(reciepe_id=id)
            recipe.delete()
            return JsonResponse({"status": "pass", "message": "Post Deleted Successfully"})
        except Recipes.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "Post not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "fail", "message": str(e)}, status=500)
class DeleteComment(APIView):
    def delete(self, request):
        comment_id = request.data.get('comment_id')
        try:
            comment = Comments.objects.get(comment_id=comment_id)
            comment.delete()
            return JsonResponse({"status": "pass", "message": "Comment Deleted Successfully"})
        except Comments.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "Comment not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "fail", "message": str(e)}, status=500)
    
class LikePost(APIView):
    def post(self, request):
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)
        recipe_id = request.POST.get('receipeId')
        recipe = get_object_or_404(Recipes, reciepe_id=recipe_id)
        like, created = Like.objects.get_or_create(user=user, recipe=recipe)

        if created:
            recipe.likes += 1
            recipe.save()
            return JsonResponse({"status": "liked", "likes": recipe.likes})
        else:
            like.delete()
            recipe.likes -= 1
            recipe.save()
            return JsonResponse({"status": "unliked", "likes": recipe.likes})

class SendRequest(APIView):
    def post(self, request):
        sender_id = request.session.get('user_id')
        userId = request.data.get('userId')
        print(sender_id,userId)
        try:
            sender_id = int(sender_id)
            userId = int(userId)    
            if sender_id == userId:
                return JsonResponse({"status":"same_user","message":'You cannot send a request to yourself'})
            sender = get_object_or_404(User, id = sender_id)
            user = get_object_or_404(User, id = userId)
            add_friend,created = FriendRequest.objects.get_or_create(reciever=user, sender=sender)
            if not created:
                return JsonResponse({"status":"fail","message":'Request Already Sent'})
            return JsonResponse({"status":"pass","message":'Request Sent Successfully'})
        except User.DoesNotExist:
            return JsonResponse({"status":"fail","message":'Failed to send'})


            
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
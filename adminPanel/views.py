from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from user.models import User
from recipes.models import Recipes,Like, Comments
from kitchen.models import Kitchen
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
class AdminDashboard(TemplateView):
    template_name = 'adminPanel/admin.html'
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('404', message='You"re not Logged In')
        return super().get(self, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')
        user = User.objects.get(id = kwargs['uid'])
        user_img = user.profilePicture
        uid = user.id
        users = User.objects.all()
        users_count = users.count()
        recipes = Recipes.objects.all()
        recipes_count = recipes.count()
        kitchen = Kitchen.objects.all()
        kitchen_count = kitchen.count()
        like = Like.objects.all()
        like_count = like.count()
        comment = Comments.objects.all()
        comment_count = comment.count()
        context['user_id']= user_id 
        context['user_name']= self.request.session.get('user_name',None) 
        context['user_email']= self.request.session.get('user_email',None)  
        context['kitchen_count'] = kitchen_count
        context['recipes_count'] = recipes_count
        context['users_count'] = users_count
        context['like_count'] = like_count
        context['comment_count'] = comment_count
        context['user_img'] = user_img
        context['uid'] = uid
        context['user'] = user
        return context
class CreateUser(TemplateView):
    template_name = 'adminPanel/create_user.html'
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('404', message='You"re not Logged In')
        return super().get(self, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')
        user = User.objects.get(id = kwargs['uid'])
        user_img = user.profilePicture
        uid = user.id
        user__name = user.username
        user__email = user.email
        users = User.objects.all()
        users_count = users.count()
        recipes = Recipes.objects.all()
        recipes_count = recipes.count()
        kitchen = Kitchen.objects.all()
        kitchen_count = kitchen.count()
        like = Like.objects.all()
        like_count = like.count()
        context['user_id']= user_id 
        context['user_name']= self.request.session.get('user_name',None) 
        context['user_email']= self.request.session.get('user_email',None)  
        context['kitchen_count'] = kitchen_count
        context['recipes_count'] = recipes_count
        context['users_count'] = users_count
        context['like_count'] = like_count
        context['user_img'] = user_img
        context['uid'] = uid
        context['user'] = user
        context['user__name'] = user__name
        context['user__email'] = user__email
        return context
class ViewAllUsers(TemplateView):
    template_name = 'adminPanel/view_user.html'
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('404', message='You"re not Logged In')
        return super().get(self, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')
        user = User.objects.get(id = kwargs['uid'])
        user_img = user.profilePicture
        uid = user.id
        users = User.objects.all()
        users_count = users.count()
        recipes = Recipes.objects.all()
        recipes_count = recipes.count()
        kitchen = Kitchen.objects.all()
        kitchen_count = kitchen.count()
        like = Like.objects.all()
        like_count = like.count()
        context['user_id']= user_id 
        context['user_name']= self.request.session.get('user_name',None) 
        context['user_email']= self.request.session.get('user_email',None)  
        context['kitchen_count'] = kitchen_count
        context['recipes_count'] = recipes_count
        context['users_count'] = users_count
        context['like_count'] = like_count
        context['user_img'] = user_img
        context['uid'] = uid
        context['users'] = users
        return context
class UpdateUser(TemplateView):
    template_name = 'adminPanel/update.html'
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('404', message='You"re not Logged In')
        return super().get(self, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')
        user = User.objects.get(id = kwargs['uid'])
        user_img = user.profilePicture
        uid = user.id
        users = User.objects.all()
        users_count = users.count()
        recipes = Recipes.objects.all()
        recipes_count = recipes.count()
        kitchen = Kitchen.objects.all()
        kitchen_count = kitchen.count()
        like = Like.objects.all()
        like_count = like.count()
        context['user_id']= user_id 
        context['user_name']= self.request.session.get('user_name',None) 
        context['user_email']= self.request.session.get('user_email',None)  
        context['kitchen_count'] = kitchen_count
        context['recipes_count'] = recipes_count
        context['users_count'] = users_count
        context['like_count'] = like_count
        context['user_img'] = user_img
        context['uid'] = uid
        context['users'] = users
        return context
class UpdatePage(TemplateView):
    template_name = 'adminPanel/update_page.html'
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('404', message='You"re not Logged In')
        return super().get(self, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')
        user = User.objects.get(id = kwargs['uid'])
        user_img = user.profilePicture
        uid = user.id
        users = User.objects.all()
        users_count = users.count()
        recipes = Recipes.objects.all()
        recipes_count = recipes.count()
        kitchen = Kitchen.objects.all()
        kitchen_count = kitchen.count()
        like = Like.objects.all()
        like_count = like.count()
        context['user_id']= user_id 
        context['user_name']= self.request.session.get('user_name',None) 
        context['user_email']= self.request.session.get('user_email',None)  
        context['kitchen_count'] = kitchen_count
        context['recipes_count'] = recipes_count
        context['users_count'] = users_count
        context['like_count'] = like_count
        context['user_img'] = user_img
        context['uid'] = uid
        context['users'] = users
        context['user'] = user
        return context
    
class UpdateUserDetails(APIView):
    def put(self, request):
        print(request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        phone = request.data.get('phone')
        first_name = request.data.get('firstname')
        last_name = request.data.get('lastname')
        date_of_birth = request.data.get('birthdate')
        role = request.data.get('role')
        nick = request.data.get('nick')
        cover_photo = request.FILES.get('cover_photo')  
        profile_image = request.FILES.get('profile')  
        user_id = request.data.get('user_id')
        is_active = request.data.get('is_active')
        try:
            user = User.objects.get(id = user_id)
            user.username = username
            user.email = email 
            user.password = password
            user.phone = phone
            user.first_name = first_name
            user.last_name = last_name
            user.role = role
            user.nick = nick
            user.date_of_birth = date_of_birth
            if profile_image:
                user.profilePicture = profile_image
            if cover_photo:
                user.cover_photo = cover_photo
            user.is_active = is_active
            user.save()
            messages.success(request, "Updated Successfully")
            return JsonResponse({"status":"pass", 'message':"Updated Successfully"})
        except User.DoesNotExist as u:
            print(u)
            return JsonResponse({"status":"fail","message":"Failed to Update"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"fail","message":str(e)})
class DeleteUser(APIView):
    def delete(self, request):
        id = request.POST['id']
        User.objects.filter(id = id).delete()
        messages.success(request, 'Deleted By Admin Successfully')
        return JsonResponse({"status":"pass"})
class DeleteAll(APIView):
    def delete(self, request):
        User.objects.all().delete()
        messages.success(request, 'Deleted All Users Successfully')
        return JsonResponse({"status":"pass"})
    

class AddUser(APIView):
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        date_of_birth = request.POST['birthdate']
        role = request.POST['role']
        nick = request.POST['nick']
        cover_photo = request.FILES.get('cover_photo')
        profile_image = request.FILES.get('profile')
        if User.objects.filter(email = email).exists():
            return JsonResponse({"status":'fail',"Error":"Email Already Exists Try with another one"})
        elif User.objects.filter(username = username).exists():
            return JsonResponse({"status":"fail","Error":"username is already taken."})
        user = User()
        user.email = email
        user.password = make_password(password)
        user.username = username
        user.phone = phone
        user.first_name = first_name
        user.last_name = last_name
        user.date_of_birth = date_of_birth
        user.profilePicture = profile_image
        if role:
            user.role = role
        if nick:
            user.nick = nick
        if cover_photo:
            user.cover_photo = cover_photo
        user.save()
        return JsonResponse({"status":"pass"})
    

class CreateKitchen(TemplateView):
    template_name = 'adminPanel/create_kitchen.html'
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('404', message='You"re not Logged In')
        return super().get(self, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')
        user = User.objects.get(id = kwargs['uid'])
        user_img = user.profilePicture
        uid = user.id
        user__name = user.username
        user__email = user.email
        users = User.objects.all()
        users_count = users.count()
        recipes = Recipes.objects.all()
        recipes_count = recipes.count()
        kitchen = Kitchen.objects.all()
        kitchen_count = kitchen.count()
        like = Like.objects.all()
        like_count = like.count()
        context['user_id']= user_id 
        context['user_name']= self.request.session.get('user_name',None) 
        context['user_email']= self.request.session.get('user_email',None)  
        context['kitchen_count'] = kitchen_count
        context['recipes_count'] = recipes_count
        context['users_count'] = users_count
        context['like_count'] = like_count
        context['user_img'] = user_img
        context['uid'] = uid
        context['user'] = user
        context['user__name'] = user__name
        context['user__email'] = user__email
        return context
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from user.models import User
from recipes.models import Recipes,Like
from kitchen.models import Kitchen
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
        user = User.objects.get(id = user_id)
        user_img = user.profilePicture
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
        return context
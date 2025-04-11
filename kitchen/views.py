from django.shortcuts import redirect, render
from rest_framework.viewsets import ModelViewSet
from friends.models import FriendRequest
from kitchen.models import Kitchen, CookingCategory, KitchenImage, KitchenVideo
from kitchen.serializers import KitchenSerializer, CookingCategorySerializer
from rest_framework.views import APIView
from django.views.generic import TemplateView
from recipes.models import Like, Recipes
from user.models import User
from django.db.models import Q , Max
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import JsonResponse
import time
from django.contrib import messages
# Create your views here.

class KitchenViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer

class CookingCategoryViewSet(ModelViewSet):
    queryset = CookingCategory.objects.all()
    serializer_class = CookingCategorySerializer

class CreateKitchen(TemplateView):
    template_name = 'kitchen/create_kitchen.html'
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('404', message='You"re not Logged In')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.session['user_name']
        user_id = self.request.session.get('user_id')
        user = User.objects.get(id=user_id)
        pending_requests = FriendRequest.objects.filter(reciever=user, status__iexact='pending')
        accepted_requests = FriendRequest.objects.filter(
                    (Q(reciever=user) | Q(sender=user)), status__iexact='accepted'
                )
        friends = set()
        for request in accepted_requests:
            if request.sender != user:
                friends.add(request.sender)
            if request.reciever != user:
                friends.add(request.reciever)
        uid = self.request.session.get('user_id')
        user = User.objects.filter(id = uid)
        reciepes = Recipes.objects.filter(user_id = uid)
        user = User.objects.filter(id = uid)
        like = Like.objects.filter(user_id = uid)
        self.request.session['post_count'] = reciepes.count()
        self.request.session['likes'] = like.count()
        context.update ({
        'userdata': user_id,
        'currentUser':user_name,
        'nick_name':self.request.session.get('user_nick_name'),
        'users':user,
        "current_user_id":self.request.session['user_id'],
        'postCount':self.request.session['post_count'],
        'like_count':self.request.session['likes'],
        'user_img':self.request.session['user_img'],
        'friends':friends,
        'pending_requests':pending_requests
        })
        return context
class AddKitchen(APIView):
    def post(self, request):
        kitchen_name = request.data.get('kitchen_name')
        website_url = request.data.get('website_url')
        business_email = request.data.get('business_email')
        location = request.data.get('location')
        user_id = request.data.get('user')
        kitchen_desc = request.data.get('kitchen_desc')
        kitchen_logo = request.FILES.get('kitchen_logo')
        user = User.objects.get(id = user_id)
        if Kitchen.objects.filter(kitchen_name__iexact = kitchen_name).exists():
            return JsonResponse({"status":"fail","message":"Kitchen Name is Already Taken"})
        elif Kitchen.objects.filter(business_email = business_email).exists():
            return JsonResponse({"status":"fail","message":"Email Already Exists"})
        elif Kitchen.objects.filter(website_url = website_url).exists():
            return JsonResponse({"status":"fail","message":"Enter an Unique URL"})
        try:
            kitchen = Kitchen()
            kitchen.kitchen_name = kitchen_name
            kitchen.website_url = website_url
            kitchen.user = user
            kitchen.business_email = business_email
            kitchen.location = location
            kitchen.kitchen_desc = kitchen_desc
            kitchen.kitchen_logo = kitchen_logo
            kitchen.save()
            return JsonResponse({"status":"pass","message":"Kitchen Created Successfully",'kitchen_id':kitchen.kitchen_id})

        except User.DoesNotExist as e:
            return JsonResponse({'status':"fail",'message':'User Does not Exist'})  
        except Exception as e:
            return JsonResponse({'status':"fail",'message':str(e)})  
class UpdateKitchen(APIView):
    def put(self, request):
        print('Request Data', request.data)
        print('Request FILES', request.FILES)
        kitchen_id = request.data.get('kitchen_id')
        kitchen_name = request.data.get('kitchen_name')
        website_url = request.data.get('website_url')
        business_email = request.data.get('business_email')
        location = request.data.get('location')
        user_id = request.data.get('user')
        kitchen_desc = request.data.get('kitchen_desc')
        kitchen_logo = request.FILES.get('kitchen_logo')
        user = User.objects.get(id = user_id)
        try:
            kitchen = Kitchen.objects.get(kitchen_id = kitchen_id)
            kitchen.kitchen_name = kitchen_name
            kitchen.website_url = website_url
            kitchen.user = user
            kitchen.business_email = business_email
            kitchen.location = location
            kitchen.kitchen_desc = kitchen_desc
            if kitchen_logo:
                kitchen.kitchen_logo = kitchen_logo
            messages.success(request, 'Kitchen Profile Updated Successfully')
            kitchen.save()
            return JsonResponse({"status":"pass","message":"Kitchen Created Successfully"})
        except User.DoesNotExist as e:
            return JsonResponse({'status':"fail",'message':'User Does not Exist'})  
        except Exception as e:
            return JsonResponse({'status':"fail",'message':str(e)})  
        
class CreateImageVideo(APIView):
        def post(self, request):
            kitchen_name = request.data.get('kitchen_name')
            kitchen = Kitchen.objects.get(kitchen_name = kitchen_name)
            try:
                kitchen_images = request.FILES.getlist('kitchen_images')
                for image in kitchen_images:
                    KitchenImage.objects.create(kitchen=kitchen, image=image)
                kitchen_videos = request.FILES.getlist('kitchen_videos')
                for video in kitchen_videos:
                    KitchenVideo.objects.create(kitchen=kitchen, video=video)
                return JsonResponse({"status":"pass",'kitchen_id':kitchen.kitchen_id})
            except Kitchen.DoesNotExist as e:
                print(e)
                return JsonResponse({"status":"fail"})
def kitchen_dashboard(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('404', message='Something Went Wrong')
    kitchen = Kitchen.objects.get(kitchen_id = id)
    kitchen_image = KitchenImage.objects.filter(kitchen = kitchen)
    kitchen_video = KitchenVideo.objects.filter(kitchen = kitchen)
    user = User.objects.get(id=user_id)
    kitchens = Kitchen.objects.all()

    recipes = Recipes.objects.filter(user_id = user)
    return render(request, 'kitchen/admin.html',{'kitchen':kitchen,'kitchen_images':kitchen_image,'recipes':recipes,"kitchens":kitchens,
'kitchen_videos':kitchen_video,"current_user_id":request.session.get('user_id',None),"currentUser":request.session.get('user_name',None)})
def recipes(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('404', message='Something Went Wrong')
    kitchen = Kitchen.objects.get(kitchen_id = id)
    kitchen_image = KitchenImage.objects.filter(kitchen = kitchen)
    kitchen_video = KitchenVideo.objects.filter(kitchen = kitchen)
    user = User.objects.get(id=user_id)
    recipes = Recipes.objects.filter(user_id = user)
    kitchens = Kitchen.objects.all()
    return render(request, 'kitchen/create.html',{'kitchen':kitchen,'kitchen_images':kitchen_image,'recipes':recipes,"kitchens":kitchens,
'kitchen_videos':kitchen_video,"current_user_id":request.session.get('user_id',None),"currentUser":request.session.get('user_name',None)})
def view_recipes(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('404', message='Something Went Wrong')
    kitchen = Kitchen.objects.get(kitchen_id = id)
    kitchen_image = KitchenImage.objects.filter(kitchen = kitchen)
    kitchen_video = KitchenVideo.objects.filter(kitchen = kitchen)
    user = User.objects.get(id=user_id)
    recipes = Recipes.objects.filter(user_id = user)
    kitchens = Kitchen.objects.all()
    return render(request, 'kitchen/view_recipes.html',{'kitchen':kitchen,'kitchen_images':kitchen_image,'recipes':recipes,"kitchens":kitchens,
'kitchen_videos':kitchen_video,"current_user_id":request.session.get('user_id',None),"currentUser":request.session.get('user_name',None)})

def create_recipe(request,id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('404', message='Something Went Wrong')
    kitchen = Kitchen.objects.get(kitchen_id = id)
    kitchen_image = KitchenImage.objects.filter(kitchen = kitchen)
    kitchen_video = KitchenVideo.objects.filter(kitchen = kitchen)
    kitchens = Kitchen.objects.all()
    return render(request, 'kitchen/create_recipe.html',{'kitchen':kitchen,'kitchen_images':kitchen_image,"kitchens":kitchens,
'kitchen_videos':kitchen_video,"current_user_id":request.session.get('user_id',None),"currentUser":request.session.get('user_name',None)})

def update_recipe(request, id, rid):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('404', message='Something Went Wrong')
    kitchen = Kitchen.objects.get(kitchen_id = id)
    kitchen_image = KitchenImage.objects.filter(kitchen = kitchen)
    kitchen_video = KitchenVideo.objects.filter(kitchen = kitchen)
    kitchens = Kitchen.objects.all()
    recipe = Recipes.objects.get(reciepe_id = rid)
    return render(request, 'kitchen/update_recipe.html', {'kitchen':kitchen,'kitchen_images':kitchen_image,"kitchens":kitchens,
'kitchen_videos':kitchen_video,"current_user_id":request.session.get('user_id',None),"currentUser":request.session.get('user_name',None), 'recipe':recipe})
        
def kitchen_profile(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('404', message='Something Went Wrong')
    kitchen = Kitchen.objects.get(kitchen_id = id)
    kitchen_image = KitchenImage.objects.filter(kitchen = kitchen)
    kitchen_video = KitchenVideo.objects.filter(kitchen = kitchen)
    kitchens = Kitchen.objects.all()
    # recipe = Recipes.objects.get(reciepe_id = rid)
    return render(request, 'kitchen/kitchen_profile.html', {'kitchen':kitchen,'kitchen_images':kitchen_image,"kitchens":kitchens,
'kitchen_videos':kitchen_video,"current_user_id":request.session.get('user_id',None),"currentUser":request.session.get('user_name',None)})

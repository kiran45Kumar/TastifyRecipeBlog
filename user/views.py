from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from django.db.models import Q
from friends.models import FriendRequest #type:ignore
from .models import User
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from recipes.models import Like, Recipes
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.parsers import JSONParser
def signup(request):
    return render(request,"user/signup.html")
def login(request):
    user_id = request.session.get('user_id', None)
    user_name = request.session.get('user_name', None)
    if user_id:
        return redirect(f'/user/{user_name}/{user_id}/posts')  
    return render(request, "user/login.html")
def index(request):
    return render(request, "user/index.html")


class LoginCheck(APIView):
    def post(self, request):
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember_me = request.POST.get("remember_me") == 'true'
            user = User.objects.get(email=email)
            if user.password != password:
                return JsonResponse({"status": "fail", "message": "Invalid Password"})
            request.session['user_name'] = user.username
            request.session['user_firstname'] = user.first_name
            request.session['user_lastname'] = user.last_name
            request.session['user_nick_name'] = user.nick
            request.session['user_id'] = user.id
            request.session['user_img'] = user.profilePicture.url if user.profilePicture else None
            user.is_logged_in = True
            user.save()
            # Set session expiry
            if remember_me:
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            else:
                request.session.set_expiry(0)  # Session expires when browser closes
            expiry_date = request.session.get_expiry_date()
            expiry_seconds = request.session.get_expiry_age()
            print(f"Session Expires At: {expiry_date}")
            print(f"Session Duration: {expiry_seconds} seconds")
            return JsonResponse({"status": "pass", "uid": user.id, 'name': user.first_name,"message":"Login Successful"})

        except User.DoesNotExist:
            return JsonResponse({"status": "no_user", "message": "Account does not exist"})
        
        except Exception as e:
            return JsonResponse({"status": "exception", "message": str(e)})


class CreateStaff(APIView):
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        date_of_birth = request.POST['birthdate']
        profile_image = request.FILES.get('profile')
        if User.objects.filter(email = email).exists():
            return JsonResponse({"status":'fail',"Error":"Email Already Exists Try with another one"})
        elif User.objects.filter(username = username).exists():
            return JsonResponse({"status":"fail","Error":"username is already taken."})
        user = User()
        user.email = email
        user.password = password
        user.username = username
        user.phone = phone
        user.first_name = first_name
        user.last_name = last_name
        user.date_of_birth = date_of_birth
        user.profilePicture = profile_image
        user.save()
        return JsonResponse({"status":"pass"})
    
class UpdateUserDetails(APIView):
    def put(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        phone = request.data.get('phone')
        first_name = request.data.get('firstname')
        last_name = request.data.get('lastname')
        date_of_birth = request.data.get('birthdate')
        # profile_image = request.FILES.get('profile')  
        user_id = request.session.get('user_id')
        
        User.objects.filter(id=user_id).update(
            email=email,
            password=password,
            username=username,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        return JsonResponse({"status":"pass"})
    
def view_user(request):
    user = User()
    uid = request.GET.get('id')
    return redirect('user_dashboard', id = uid)

def user_dashboard(request,name, id):
    user_id = get_object_or_404(User,id = id)
    user_name = request.session['user_name']
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
    uid = request.session['user_id']
    user = User.objects.filter(id = uid)
    reciepes = Recipes.objects.filter(user_id = uid)
    user = User.objects.filter(id = uid)
    like = Like.objects.filter(user_id = uid)
    request.session['post_count'] = reciepes.count()
    request.session['likes'] = like.count()
    context = {
        'userdata': user_id,
        'currentUser':user_name,
        'nick_name':request.session.get('user_nick_name'),
        'users':user,
        "current_user_id":request.session['user_id'],
        'postCount':request.session['post_count'],
        'like_count':request.session['likes'],
        'user_img':request.session['user_img'],
        'friends':friends,
        'pending_requests':pending_requests
    }
    return render(request, 'user/userdashboard.html', context)


def check_online_status(request):
    user_id = request.session.get('user_id')  # Get logged-in user ID
    if not user_id:
        return redirect('404', message = 'User Not Loggedin')
    user = User.objects.get(id=user_id)
    accepted_requests = FriendRequest.objects.filter(
        (Q(reciever=user) | Q(sender=user)), status__iexact='accepted'
    )

    friends = []
    for request in accepted_requests:
        friend = request.sender if request.sender != user else request.reciever
        friends.append({
            'id': friend.id,
            'username': friend.username,
            'profilePicture': friend.profilePicture.url if friend.profilePicture else None,
            'is_logged_in': friend.is_logged_in,  # Online status
        })
    return JsonResponse({'friends': friends})


class ViewStaff(TemplateView):
    template_name = 'view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userdata = User.objects.all()
        context['userdata'] = userdata
        return context
class DeleteUser(APIView):
    def post(self, request):
        id = request.POST['id']
        User.objects.filter(id = id).delete()
        return JsonResponse({"status":"pass"})
class LogoutUser(APIView):
    def post(self, request):
        user_id = request.session.get('user_id',None)
        user = User.objects.get(id=user_id)
        print(f"User: {user.username} has been logged out")
        user.is_logged_in = False
        user.save()
        request.session.flush()
        return JsonResponse({"status":"pass"})
def not_found(request,message):
    return render(request, "404/404.html", {"error":message})

class AddNickName(APIView):
    def post(self, request):
        nick_name = request.POST.get('nick_name')
        user_id = request.session.get('user_id')
        user = User.objects.get(id= user_id)
        user.nick = nick_name
        user.save()
        return JsonResponse({'status':"pass"})
class SaveImg(APIView):
    def post(self, request):
        img = request.FILES.get('img')
        user_id = request.session.get('user_id')
        user = User.objects.get(id = user_id)
        user.profilePicture = img
        user.save()
        return JsonResponse({'status':"pass"})
class UploadCoverImg(APIView):
    def post(self, request):
        img = request.FILES.get('cover_img')
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id = user_id)
            user.cover_photo = img
            user.save()
            return JsonResponse({'status':"pass"})
        except User.DoesNotExist:
            return JsonResponse({'status':"fail"})
        except Exception as e:
            return JsonResponse({'status':"fail"})
def user_details(request, id):
    try:
        user = get_object_or_404(User, id=id)
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/')
        user_u = User.objects.get(id=user_id)
        pending_requests = FriendRequest.objects.filter(reciever=user_u, status__iexact='pending')
        users = User.objects.filter(id=id)
        recipes = Recipes.objects.filter(user_id=user)
        recipe_count = recipes.count()
        return render(request, 'user/user_details.html', {
            'user': user,
            'users': users,
            'currentUser': request.session.get('user_name', None),
            'nick_name': request.session.get('user_nick_name', None),
            'current_user_id': user_id,
            'recipes': recipes,
            'recipe_count': recipe_count,
            'pending_requests': pending_requests
        })
    except User.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)

def forgot_password(request):
    return render(request, 'user/forgot_password.html')

class SendMail(APIView):
    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email = email)
            user_exists = True
            if user_exists:
                send_mail(
                subject="Hello from Tastify",
                message=f'Thanks for reaching us out. Here is your link to reset the password link: http://127.0.0.1:5000/reset_password/{user.id}',    
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            return JsonResponse({'status':'fail','message':'User Does not exist'})
        except Exception as e:
            return JsonResponse({'status':'fail','message':"Network Error"})
        return JsonResponse({'status':'pass', 'message':'Please Check Your Email'})
def reset_password(request, id):
    user = get_object_or_404(User, id = id)
    return render(request, 'user/reset_password.html', {'user':user})
class ChangePassword(APIView):
    def post(self, request):
        id = request.data.get('user_id')
        password = request.data.get('newpassword')
        try:
            user = User.objects.get(id = id)
            user.password = password
            user.save()
        except User.DoesNotExist:
            return JsonResponse({'status':'fail','message':'User Does not exist'})
        except Exception as e:
            return JsonResponse({'status':'exception','message':str(e)})
        return JsonResponse({'status':'pass', "message":"Password Changed Successfully"})

class IncrementRecipeView(APIView):
    def post(self, request):
        try:
            print(request.data)
            # data = JSONParser().parse(request)
            reciepe_id = request.data.get('reciepe_id')
            if not reciepe_id:
                return JsonResponse({'status': 'fail', 'message': 'Recipe ID missing'}, status=400)
            recipe = Recipes.objects.get(reciepe_id = reciepe_id)
            recipe.views += 1
            recipe.save()
            return JsonResponse({'status':'pass','views':recipe.views})
        except Recipes.DoesNotExist:
            return JsonResponse({'status':'fail','message':'Recipe Not Found'}, status = 404)
        except Exception as e:
            return JsonResponse({'status':'fail', 'message':str(e)},status=500)
# class AddFriend(APIView):
#     def post(self, request):
#         friend_id = request.data.get('user_id')
#         pass

def friends(request):
    user_id = request.session.get('user_id')
    currentUser = request.session.get('user_name')
    if not user_id:
        return redirect('/')
    user = User.objects.get(id = user_id)
    pending_requests = FriendRequest.objects.filter(reciever=user, status__iexact='pending')
    accepted_friends = FriendRequest.objects.filter(
        (Q(sender_id=user_id) | Q(reciever_id=user_id)),
        status='accepted'
    ).values_list('sender_id', 'reciever_id')

    accepted_user_ids  = set()
    for sender_id, receiver_id in accepted_friends:
        accepted_user_ids .add(sender_id)
        accepted_user_ids .add(receiver_id)
    allUsers = User.objects.exclude(id__in=accepted_user_ids).exclude(id=user_id)    
    users = User.objects.filter(id = user_id)
    return render(request, 'friends/friends.html', {'users':users, 'currentUser':currentUser, 'allUsers':allUsers, 'current_user_id':user_id, 'nick_name':request.session.get('user_nick_name'),'pending_requests':pending_requests})

class ViewRequests(TemplateView):
    template_name = 'friends/my_friends.html'
    
    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')
        print(user_id)
        users = User.objects.filter(id = user_id)
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
        print(f"Pending Requests: {pending_requests}")  # Debugging
        print(f"Accepted Friends: {friends}")  # Debugging

        context['pending_requests'] = pending_requests
        context['friends'] = friends
        context['currentUser'] = self.request.session.get('user_name')
        context['users'] = users
        context['current_user_id'] = self.request.session.get('user_id', None)
        context['nick_name'] = self.request.session.get('user_nick_name')
        return context

    
class AcceptRequest(APIView):
    def post(self, request):
        request_id = request.POST.get('user_id')
        request_status = request.POST.get('status')
        print(request_id,request_status)
        try:
            FriendRequest.objects.filter(id=request_id).update(status = "accepted" if request_status == "pending" else "rejected")
            return JsonResponse({'status': 'pass', 'message': 'Friend request accepted'})
        except FriendRequest.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Friend request not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)
    
class RejectRequest(APIView):
    def post(self, request):
        request_id = request.POST.get('user_id')
        request_status = request.POST.get('status')
        print(request_id,request_status)
        try:
            FriendRequest.objects.filter(id=request_id).update(status = "rejected" if request_status == "pending" else "pending")
            return JsonResponse({'status': 'pass', 'message': 'Friend request Rejected'})
        except FriendRequest.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Friend request not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)
class RemoveFriend(APIView):
    def delete(self, request):
        friend_id = request.POST.get('friend_id')
        user_id = request.session.get('user_id')
        print(friend_id,user_id)
        try:
            friend_request = FriendRequest.objects.filter(
                Q(sender__id=user_id, reciever__id=friend_id) | Q(sender__id=friend_id, reciever__id=user_id)
            )
            friend_request.delete()
            return JsonResponse({'status': 'pass', 'message': 'Friend removed successfully'})
        except FriendRequest.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Friend request not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)
def update_user(request, id):
    user = get_object_or_404(User, id=id)
    pending_requests = FriendRequest.objects.filter(reciever=user, status__iexact='pending')
    users = User.objects.filter(id = id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.date_of_birth = request.POST['birthdate']
        user.profilePicture = request.FILES.get('profile')
        user.save()
        return redirect('view_user')
    return render(request, 'user/update_user.html', {
        'user': user,'currentUser':request.session.get('user_name'), 'nick_name':request.session.get('user_nick_name'),
          'current_user_id':request.session.get('user_id',None), 'users':users,'pending_requests':pending_requests
          })

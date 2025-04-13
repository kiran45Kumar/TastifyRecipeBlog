from django.urls import path
from adminPanel.views import *
urlpatterns = [
    path('admin_dashboard/<int:uid>', AdminDashboard.as_view(), name='admin_dashboard'),
    path('create_user/<int:uid>', CreateUser.as_view(), name='create_user'),
    path('add_user/', AddUser.as_view(), name='create_user'),
    path('view_user/<int:uid>', ViewAllUsers.as_view(), name='view_user'),
    path('update_user/<int:uid>', UpdateUser.as_view(), name='update_user'),
    path('update_page/<int:uid>', UpdatePage.as_view(), name='update_page'),
    path('update_user/', UpdateUserDetails.as_view(), name='update_user'),
    path('delete_user_admin/', DeleteUser.as_view(), name='delete_user_admin'),
    path('delete_all/', DeleteAll.as_view(), name='DeleteAll'),
    path('create_kitchen_admin/<int:uid>', CreateKitchen.as_view(), name='create_kitchen'),
    path('add_kitchen_admin/', AddKitchenAdmin.as_view(), name='add_kitchen_admin'),
]
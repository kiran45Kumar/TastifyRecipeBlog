from django.urls import path
from adminPanel.views import *
urlpatterns = [
    path('admin_dashboard/<int:uid>', AdminDashboard.as_view(), name='admin_dashboard')
]
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
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
        context['user_id']= user_id
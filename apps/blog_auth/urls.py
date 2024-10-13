from django.urls import path
from django.views.generic import TemplateView
from views import *

app_name = 'apps.blog_auth'

urlpatterns = [
    path('registro',SignUpView.as_view(), name='registro'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('registrocompletado', TemplateView.as_view(
        template_name = 'auth/registrocompleto.html'),
        name='registrocompleto')
    #path('login', login_view, name='login')
]
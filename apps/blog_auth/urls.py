from django.urls import path
from django.views.generic import TemplateView
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView, LoginView, LogoutView, CustomLoginView
from myblog.views import index

app_name = 'apps.blog_auth'

urlpatterns = [
    path('registro',SignUpView.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register'),
]
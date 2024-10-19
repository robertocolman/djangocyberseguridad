from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from .forms import SignUpForm
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout


class Login(auth_views.LoginView):
    template_name = "auth/login.html"
    
class SignUpView(FormView):
    template_name = 'auth/registro.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'  # Asegúrate de que esta sea la ruta correcta a tu plantilla
    success_url = reverse_lazy('index')


'''def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("apps.blog_auth:login")
        else:
            messages.error(request, "Credenciales incorrectas")
    return render(render, "auth/login.html")'''

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = "auth/logout.html"
    next_page = reverse_lazy('blog:index')

# class Logout(LoginRequiredMixin,auth_views.LogoutView):
#     ''' Vista de Cierre sesión de Usuario '''
#     template_name = "auth/logout.html"

# def LogoutView(request):
#     logout(request)
#     return redirect('apps.blog:index')


    
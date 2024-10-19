from sqlite3 import IntegrityError
from django import forms
from django.urls import reverse_lazy
from apps.blog.models import Post, Comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .views import *
from django.views.generic import FormView
from django.contrib.auth import login
from .models import Perfil

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields =(
            'username',
            'email',
            'password1',
            'password2'
        )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'resumen', 'contenido', 'imagen', 'categorias']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['cuerpo_comentario']
        widgets = {
            'cuerpo_comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SignUpView(FormView):
    template_name = 'auth/registro.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')  # Redirigir al index después del registro

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Loguear automáticamente al usuario
        return redirect(self.success_url)
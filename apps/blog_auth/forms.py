from django import forms
from apps.blog.models import Post, Comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
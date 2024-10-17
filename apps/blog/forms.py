from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'categoria']  # Asegúrate de usar 'categoria'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del artículo'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Contenido del artículo'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

# class ComentarioForm(forms.ModelForm):
#     class Meta:
#         model = Comentario
#         fields = ['cuerpo_comentario']
#         widgets = {
#             'cuerpo_comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }
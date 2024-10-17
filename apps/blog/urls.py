from django.urls import path
from django.urls.conf import include
from apps.blog.views import *

app_name = 'apps.blog'

urlpatterns = [
    path("", index, name='index'),
    path("contacto", contacto, name='contacto'),
    path("formulario", formulario, name='formulario'),
    path("posts", lista_posts, name='lista_posts'),
    path('posts/crear/', crear_post, name='crear_post'),
    path('posts/<int:pk>/', postdetalle, name='postdetalle'),
    path('editar/<int:pk>/', editar_post, name='editar_post'),  # Usamos pk aquí
    path('eliminar/<int:pk>/', eliminar_post, name='eliminar_post'),
    path('posts/<int:pk>/', postdetalle, name='postdetalle'),
]
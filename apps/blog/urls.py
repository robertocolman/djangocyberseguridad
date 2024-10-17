from django.urls import path
from django.urls.conf import include
from apps.blog.views import *
from . import views

app_name = 'apps.blog'

urlpatterns = [
    path("", views.index, name='index'),
    path("contacto", contacto, name='contacto'),
    path("formulario", formulario, name='formulario'),
    path("posts", lista_posts, name='lista_posts'),
    path("posts-detalle/<int:id>/", postdetalle, name='postdetalle'),
    path('posts/crear/', crear_post, name='crear_post'),  # Asegúrate de que esta línea esté presente
    path('editar/<int:pk>/', editar_post, name='editar_post'),  # Usamos pk aquí
    path('eliminar/<int:pk>/', eliminar_post, name='eliminar_post'), 
    path('post/<int:id>/', views.postdetalle, name='postdetalle'),
]
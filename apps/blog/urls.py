from django.urls import path
from django.urls.conf import include
from apps.blog.views import *

app_name = 'apps.blog'

urlpatterns = [
    path("", index, name='index'),
    path("contacto", contacto, name='contacto'),
    path("formulario", formulario, name='formulario'),
    path("posts", lista_posts, name='lista_posts'),
    path("posts-detalle/<int:id>/", postdetalle, name='postdetalle'),
    path('posts/crear/', crear_post, name='crear_post'),  # Asegúrate de que esta línea esté presente
    path('editar/<int:post_id>/', editar_post, name='editar_post'),
    path('eliminar/<int:post_id>/', eliminar_post, name='eliminar_post'),
]
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
]
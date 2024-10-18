from django.urls import path
from django.urls.conf import include
from apps.blog.views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import postdetalle, eliminar_comentario

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
    path('posts/<int:pk>/marcar-favorito/', marcar_favorito, name='marcar_favorito'),
    path('posts/<int:pk>/desmarcar-favorito/', desmarcar_favorito, name='desmarcar_favorito'),
    path('favoritos/', lista_favoritos, name='lista_favoritos'),
    path('post/<int:pk>/', views.postdetalle, name='postdetalle'),
    path('post/<int:pk>/', postdetalle, name='postdetalle'),
    path('comentario/eliminar/<int:comentario_id>/', eliminar_comentario, name='eliminar_comentario'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
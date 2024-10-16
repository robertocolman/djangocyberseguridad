#from django.http import HttpResponse
#from django.views import View
#from django.views.generic import TemplateView
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Comentario
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from apps.blog_auth.forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def index(request):
    ultimosposts=Post.objects.all().order_by('fecha_publicacion').reverse()[:3]
    return render(request, 'index.html', {'ultimosposts':ultimosposts})

def index(request):
    return render(request, 'index.html')

def contacto(request):
    return render(request, 'contacto.html')

def formulario(request):
    return render(request, 'formulario.html')

class Login(auth_views.LoginView):
    template_name = "auth/login.html"

def lista_posts(request):
    #posts = Post.objects.filter(fecha_publicacion=timezone.now()).order_by('fecha_publicacion')
    posts=Post.objects.all().order_by('fecha_publicacion')
    return render(request, 'posts.html',{'posts':posts})

def postdetalle(request,id):
    try:
        data = Post.objects.get(id=id)
        comentarios = Comentario.objects.filter(aprobado=True)
    except Post.DoesNotExist:
        raise Http404('El Post seleccionado no existe.')
    
    comentarios = Comentario.objects.filter(aprobado=True)
    context={
        "post": data,
        "comentarios": comentarios
    }
    return render(request, 'post_detalle.html', context)

@login_required
def crear_post(request):
    if request.user.perfil.rol == 'colaborador':
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)  # Maneja archivos (imágenes)
            if form.is_valid():
                nuevo_post = form.save(commit=False)  # Crea el post sin guardarlo
                nuevo_post.autor = request.user  # Asigna el autor del post
                nuevo_post.save()  # Guarda el post en la base de datos
                return redirect('nombre_de_la_vista_de_exito')  # Redirige a una vista de éxito
        else:
            form = PostForm()  # Crea un formulario vacío para el GET

        return render(request, 'blog/crear_post.html', {'form': form})  # Renderiza la plantilla con el formulario
    else:
        return HttpResponseForbidden("No tienes permisos para crear un post.")

@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user.perfil.rol == 'colaborador' or request.user == post.autor:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('nombre_de_la_vista_de_exito')  # Cambia esto por la vista deseada
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/editar_post.html', {'form': form, 'post': post})
    else:
        return HttpResponseForbidden("No tienes permisos para editar este post.")

@login_required
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user.perfil.rol == 'colaborador' or request.user == post.autor:
        post.delete()
        return redirect('nombre_de_la_vista_de_exito')  # Cambia esto por la vista deseada
    else:
        return HttpResponseForbidden("No tienes permisos para eliminar este post.")




''' def home_view(request):
    return HttpResponse("Esto es una página de prueba!")

def index(request):
    return render(request, 'inicio.html')

class IndexView(View):
    def get(self, request):
        return HttpResponse("Esta es la página principal")

class AboutView(TemplateView):
    #pass
    template_name = 'inicio.html'
'''



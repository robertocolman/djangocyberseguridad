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
from apps.blog_auth.forms import ComentarioForm


# Create your views here.
def index(request):
    ultimosposts=Post.objects.all().order_by('fecha_publicacion').reverse()[:3]
    return render(request, 'index.html', {'ultimosposts':ultimosposts})

def base_view(request):
    favoritos = request.user.favoritos.all() if request.user.is_authenticated else []
    return render(request, 'base.html', {'favoritos': favoritos})

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
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posts = Post.objects.filter(categoria_id=categoria_id)
    else:
        posts = Post.objects.all()
    
    return render(request, 'posts.html', {'posts': posts})

def postdetalle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comentarios = Comentario.objects.filter(post=post, aprobado=True)

    # Procesar el formulario de comentarios si se envía a través de POST
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.autor_comentario = request.user
            comentario.save()
            return redirect('apps.blog:postdetalle', pk=pk) 
    else:
        form = ComentarioForm()

    context = {
        "post": post,
        "comentarios": comentarios,
        "form": form,
    }

    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.post = post
        comentario.autor_comentario = request.user
        comentario.save()
        print("Comentario guardado:", comentario)  # Debug: Verifica el comentario
        return redirect('apps.blog:postdetalle', pk=pk)

    return render(request, 'post_detalle.html', context)

    

@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES para manejar imágenes
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user  # Asociar el post al usuario actual
            post.save()
            return redirect('apps.blog:lista_posts')  # Redirigir a la lista de posts
    else:
        form = PostForm()  # Crear una nueva instancia del formulario

    return render(request, 'crear_post.html', {'form': form})

@login_required
def editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk, autor=request.user)  # Solo permite que el autor edite su post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('apps.blog:postdetalle', pk=post.pk)  # Cambia 'id' por 'pk'
    else:
        form = PostForm(instance=post)
    return render(request, 'editar_post.html', {'form': form})

@login_required
def eliminar_post(request, pk):
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:lista_posts')
    return render(request, 'eliminar_post.html', {'post': post})

@login_required
def marcar_favorito(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.favoritos.add(request.user)
    return redirect('apps.blog:postdetalle', pk=pk)

@login_required
def desmarcar_favorito(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.favoritos.remove(request.user)
    return redirect('apps.blog:postdetalle', pk=pk)

@login_required
def lista_favoritos(request):
    favoritos = request.user.favoritos.all()  # Obtiene los posts favoritos del usuario
    return render(request, 'lista_favoritos.html', {'favoritos': favoritos})

def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    # Verificar que el usuario sea el autor del comentario
    if request.user == comentario.autor_comentario:
        comentario.delete()  # Eliminar el comentario

    return redirect('apps.blog:postdetalle', pk=comentario.post.id)




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



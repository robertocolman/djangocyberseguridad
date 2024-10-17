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
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posts = Post.objects.filter(categoria_id=categoria_id)
    else:
        posts = Post.objects.all()
    
    return render(request, 'posts.html', {'posts': posts})

def postdetalle(request, pk):
    try:
        data = Post.objects.get(id=pk)  # Cambia 'id' a 'pk'
        comentarios = Comentario.objects.filter(post=data, aprobado=True)  # Filtrar comentarios por el post
    except Post.DoesNotExist:
        raise Http404('El Post seleccionado no existe.')

    context = {
        "post": data,
        "comentarios": comentarios
    }
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



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
    # ultimosposts=Post.objects.all().order_by('fecha_publicacion').reverse()[:3]
    ultimosposts = Post.objects.all().order_by('-fecha_publicacion')
    context = {
        'ultimosposts': ultimosposts
    }
    return render(request, 'index.html', context)

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

def postdetalle(request,id):
    try:
        data = Post.objects.get(id=id)
        comentarios = Comentario.objects.filter(aprobado=True)
    except Post.DoesNotExist:
        raise Http404('El Post seleccionado no existe.')
    
    # post = get_object_or_404(Post, id=id)
    comentarios = Comentario.objects.filter(aprobado=True) 

    # if request.method == 'POST':
    #     if request.user.is_authenticated:
    #         form = ComentarioForm(request.POST)
    #         if form.is_valid():
    #             comentario = form.save(commit=False)
    #             comentario.post = post
    #             comentario.autor = request.user
    #             comentario.save()
    #             return redirect('postdetalle', id=post.id)
    #     else:
    #         return redirect('login')
    # else:
    #     form = ComentarioForm()
    
    context={
        "post": data,
        "comentarios": comentarios,
        # 'form': form,
    }
    return render(request, 'post_detalle.html', context)



    context = {
        'post': post,
        'comentarios': comentarios,
        'form': form,
    }
    
    return render(request, 'post_detalles.html', context)

@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES para manejar imágenes
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user  # Asociar el post al usuario actual
            post.save()
            return redirect('apps.blog:index')  # Redirigir a la lista de posts
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
            return redirect('blog:postdetalle', id=post.pk)  # Corrige el nombre de la vista si es necesario
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


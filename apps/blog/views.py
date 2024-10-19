from django.http.response import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Comentario, Categoria
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from apps.blog_auth.forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from apps.blog_auth.forms import ComentarioForm
from django.views.generic import DetailView
from .forms import CrearPostForm
from django.views import View


# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('fecha_publicacion').reverse()[:3] 
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    return render(request, 'index.html', {'posts': posts, 'categorias': categorias})
    # Obtiene los últimos 3 posts, ordenados por fecha de publicación (más recientes primero)
#    ultimosposts = Post.objects.all() 
    # Obtiene todas las categorías
#    categorias = Categoria.objects.all()
     # Pasa los posts y categorías al contexto
"""    context = {
        'ultimosposts': ultimosposts,
        'categorias': categorias,
    }
    return render(request, 'index.html', context)

 return render(request, 'index.html', {'ultimosposts': ultimosposts})
    return render(request, 'index.html', {context}) 
"""

def base_view(request):
    favoritos = request.user.favoritos.all() if request.user.is_authenticated else []
    return render(request, 'base.html', {'favoritos': favoritos})

#def index(request):
    

def contacto(request):
    return render(request, 'contacto.html')

def formulario(request):
    return render(request, 'formulario.html')

class Login(auth_views.LoginView):
    template_name = "auth/login.html"

def lista_posts(request):
    #posts = Post.objects.filter(fecha_publicacion=timezone.now()).order_by('fecha_publicacion')
    posts=Post.objects.all().order_by('fecha_publicacion')
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posts = Post.objects.filter(categoria_id=categoria_id)
    else:
        posts = Post.objects.all()
    
    return render(request, 'posts.html', {'posts': posts, 'categorias': categorias})

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


def categoria_posts(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(categorias=categoria)  # Filtra los posts por la categoría seleccionada
    categorias = Categoria.objects.all()  # Obtener todas las categorías para mostrar en la plantilla

    context = {
        'categoria': categoria,
        'posts': posts,
        'categorias': categorias,  # Agregar las categorías al contexto
    }
    return render(request, 'blog/posts.html', context)

def posts(request):
    posts = Post.objects.all()  # Obtener todos los posts
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    return render(request, 'posts.html', {'posts': posts, 'categorias': categorias})

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detalles.html'  # Asegúrate de que esta plantilla exista
    context_object_name = 'post'

@login_required
def toggle_favorite(request, post_id):
    post = Post.objects.get(id=post_id)
    
    if request.user.perfil.favoritos.filter(id=post_id).exists():
        # Si ya es favorito, lo removemos
        request.user.perfil.favoritos.remove(post)
        is_favorite = False
    else:
        # Si no es favorito, lo agregamos
        request.user.perfil.favoritos.add(post)
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})

def borrar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    post_id = comentario.post.id  # Obtén el ID del post al que pertenece el comentario
    if request.method == 'POST':
        if request.user == comentario.autor_comentario:
            comentario.delete()
            return redirect('apps.blog:post_detalle', pk=post_id)  # Redirige al detalle del post
    return redirect('apps.blog:post_detalle', pk=post_id)

class CrearPostView(View):
    def get(self, request):
        form = CrearPostForm()
        return render(request, 'blog/crear_post.html', {'form': form})

    def post(self, request):
        form = CrearPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user  # Asigna el autor del post
            post.save()  # Guarda el post primero para que se pueda asociar con las categorías
            form.save_m2m()  # Guarda las relaciones de categorías (ManyToMany)
            return redirect('apps.blog:posts')  # Redirige después de crear el post
        return render(request, 'blog/crear_post.html', {'form': form})
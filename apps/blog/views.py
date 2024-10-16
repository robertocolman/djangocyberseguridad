#from django.http import HttpResponse
#from django.views import View
#from django.views.generic import TemplateView
from django.http.response import Http404
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comentario

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



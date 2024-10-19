from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

 
# Create your models here.
class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo= models.CharField(max_length=200)
    resumen= models.TextField()
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='post/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    categorias = models.ManyToManyField('Categoria', related_name='posts')
    favoritos = models.ManyToManyField(User, related_name='favoritos', blank=True)

    def publicar(self):
        self.fecha_publicacion = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo
    
    def mostrarComentarios(self):
        return self.comentarios.filter(aprobado=True)

class Categoria(models.Model):
    nombre=models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
 
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    autor_comentario = models.ForeignKey(User, on_delete=models.CASCADE)
    cuerpo_comentario = models.TextField()
    creado = models.DateTimeField(auto_now_add=True) #¿por qué? 
    aprobado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)  # Fecha de creación del comentario

    def __str__(self):
        return f'Comentario por {self.autor_comentario} en {self.post}'

    class Meta:
        ordering = ['-creado']

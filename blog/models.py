from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo= models.CharField(max_length=200)
    resumen= models.TextField()
    contenido = models.TextField()
    imagen = models.ImageField(null=True, blank=True, upload_to='img/posts', help_text='Seleccione una imagen para mostrar')
    fecha_creacion=models.DateTimeField(default=timezone.now())
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    categorias = models.ManyToManyField('Categoria', related_name='posts')

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
    post = models.ForeignKey('Post', related_name='comentarios', on_delete=models.CASCADE)
    autor_comentario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cuerpo_comentario = models.TextField()
    fch_creado = models.DateTimeField(default=timezone.now())
    aprobado = models.BooleanField(default=False) 

    def aprobarComentario(self):
        self.aprobado=True
        self.save()

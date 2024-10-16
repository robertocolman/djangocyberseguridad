from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    USUARIO_ROLES = (
        ('visitante', 'Visitante'),
        ('miembro', 'Miembro'),
        ('colaborador', 'Colaborador'),
    )

    rol = models.CharField(max_length=50, choices=USUARIO_ROLES, default='visitante')

    def __str__(self):
        return self.user.username
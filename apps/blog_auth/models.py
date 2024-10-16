from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    USUARIO_ROLES = (
        ('visitante', 'Visitante'),
        ('miembro', 'Miembro'),
        ('colaborador', 'Colaborador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50, choices=USUARIO_ROLES, default='visitante')

    def __str__(self):
        return self.user.username
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, update_last_login
from .models import Perfil

# @receiver(post_save, sender=User)
# def crear_perfil(sender, instance, created, **kwargs):
#     if created:  # Solo crea el perfil si el usuario es nuevo
#         Perfil.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def guardar_perfil(sender, instance, **kwargs):
#     instance.perfil.save()


@receiver(post_save, sender=User)
def registrar_login(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(user=instance)

# @receiver(post_save, sender=User)
# def crear_perfil(sender, instance, created, **kwargs):
#     if created:
#         Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):  # Asegúrate de que el perfil exista antes de guardarlo
        instance.perfil.save()

# @receiver(post_save, sender=User)
# def guardar_perfil(sender, instance, created, **kwargs):
#     if created:  # Solo crea un perfil si el usuario es nuevo
#         Perfil.objects.create(user=instance)
#     else:
#         # Aquí podrías actualizar el perfil si es necesario
#         perfil = instance.perfil  # Acceder al perfil asociado al usuario
#         perfil.save()  # Guardar cualquier cambio si es necesario
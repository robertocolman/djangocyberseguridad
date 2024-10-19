from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, update_last_login
from .models import Perfil

# @receiver(post_save, sender=User)
# def crear_perfil(sender, instance, created, **kwargs):
#     if created and not hasattr(instance, 'perfil'):
#         Perfil.objects.create(user=instance)
#     else:
#         pass

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    instance.perfil.save()




# @receiver(post_save, sender=User)
# def crear_perfil(sender, instance, created, **kwargs):
#     if created:
#         # Solo crear perfil si el usuario es nuevo
#         Perfil.objects.create(user=instance)
#     else:
#         # Si el perfil ya existe, actualizarlo en lugar de crearlo
#         instance.perfil.save()

# @receiver(post_save, sender=User)
# def crear_perfil(sender, instance, created, **kwargs):
#     if created:
#         # Usamos get_or_create para evitar duplicados
#         perfil, creado = Perfil.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    instance.perfil.save()
from base import *

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nombre_database',
        'USER': 'nombre_usuario_db',
        'PASSWORD': 'usuario_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

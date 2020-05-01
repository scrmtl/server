import os
from scrumtool.settings.common import *


POSTGRES_HOST = os.getenv('POSTGRES_HOST',
                          'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD',
                              'postgresistdasbestedockerimage')
POSTGRES_USER = os.getenv('POSTGRES_USER',
                          'scrmtladmin')
POSTGRES_DB = os.getenv('POSTGRES_DB',
                        'scrumtooldb')
POSTGRES_PORT = os.getenv('POSTGRES_PORT',
                          '5432')

DEBUG = True

# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = '725#n#v8bw-nw8_pd3zcos)l-o13)ua4uju(64pbj5z*8ryr(x'

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['scrmtl.ddns.net',
                 'elherminius.ddns.net',
                 'localhost']

# https://stackoverflow.com/questions/56916448/access-control-allow-origin-issue-in-vue-js-and-django
CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
    }
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': (
        'rest_framework.schemas.coreapi.AutoSchema'),
}

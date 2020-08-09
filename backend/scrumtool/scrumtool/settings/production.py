import os
from scrumtool.settings.common import *

DEBUG = True

# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = '725#n#v8bw-nw8_pd3zcos)l-o13)ua4uju(64pbj5z*8ryr(x'

# SECURITY WARNING: update this when you have the production host
# 'BACKEND_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'BACKEND_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.getenv('BACKEND_ALLOWED_HOSTS', 'localhost').split(' ')

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
OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'}
}

AUTH_USER_MODEL = 'api.ScrumUser'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': (
        'rest_framework.schemas.coreapi.AutoSchema'),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )

}
# Needed for reverse proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Support subdirectory setup behind proxy
webroot = os.getenv('OVERWRITEWEBROOT')
FORCE_SCRIPT_NAME = webroot
SESSION_COOKIE_PATH = webroot
LOGIN_REDIRECT_URL= webroot
LOGOUT_REDIRECT_URL= webroot
STATIC_FILES_URL= str(webroot) + str('static/')
MEDIA_FILES_URL= str(webroot) + str('media/')
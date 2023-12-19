from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


CORS_ORIGIN_ALLOW_ALL = True



CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

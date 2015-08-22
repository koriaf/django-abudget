from .base import *  # NOQA

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'abudget.db',
    }
}

SECRET_KEY = '?'

CRISPY_FAIL_SILENTLY = True

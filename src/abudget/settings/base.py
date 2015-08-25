# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'crispy_forms',
    'widget_tweaks',

    'abudget',
    'abudget.money',
    'abudget.users',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'abudget.money.middleware.ProvideBudgetMiddleware',
)

ROOT_URLCONF = 'abudget.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'abudget.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# defined in local.py or prod.py, pointless here.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'abudget',
#         'USER': 'abudget',
#         'PASSWORD': 'abudget',
#         'HOST': 'localhost',
#         'PORT': '',
#         'ATOMIC_REQUESTS': True,
#     }
# }

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)
USE_I18N = True

USE_L10N = False
DATE_FORMAT = "d.m.Y"
DATETIME_FORMAT = "d.m.Y H:i"
TIME_FORMAT = "H:i"

USE_TZ = True
TIME_ZONE = 'Europe/Moscow'


STATIC_URL = '/static/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

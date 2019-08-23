import os
from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = env.bool('AB_DEBUG', default=True)
SECRET_KEY = env('AB_SECRET_KEY', default="DefaultSecretKey")

ALLOWED_HOSTS = ['*']

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
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT', default=5432),
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'ATOMIC_REQUESTS': True,
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
)
USE_I18N = True
USE_L10N = False
DATE_FORMAT = "d.m.Y"
DATETIME_FORMAT = "d.m.Y H:i"
TIME_FORMAT = "H:i"

USE_TZ = True
TIME_ZONE = env('AB_TIMEZONE', default='Europe/Moscow')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/src/node_modules',
)

# for collectstatic
STATIC_ROOT = env(
    'AB_STATIC_ROOT',
    default=os.path.join(BASE_DIR, "/var/static_root")
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

RAVEN_DSN = env('AB_RAVEN_DSN', default=None)
if RAVEN_DSN:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN,
    }

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10 * 1000

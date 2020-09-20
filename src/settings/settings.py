import os
import socket
import sys
from datetime import timedelta

from celery.schedules import crontab

from django.urls import reverse_lazy


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # test_task/src - folder

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['SERVER'] == 'dev'

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(':')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # pip installed
    'django_extensions',
    'django_registration',
    'crispy_forms',
    'rest_framework',
    'drf_yasg',
    'corsheaders',

    # own
    'account',
    'pages',
    'book',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'account', 'templates'),
            os.path.join(BASE_DIR, 'pages', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'active_link_tags': 'pages.templatetags.active_link_tags',
                'alerts': 'pages.templatetags.alerts',
                'utils': 'pages.templatetags.utils',
            }
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
    },
}

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
REDIS_CACHE_LOCATION = os.environ['REDIS_CACHE_LOCATION']
REDIS_BROKER_LOCATION = os.environ['REDIS_BROKER_LOCATION']
REDIS_URI = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/"

CELERY_BROKER_URL = REDIS_URI + REDIS_BROKER_LOCATION

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URI + REDIS_CACHE_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

CELERY_BEAT_SCHEDULE = {
    'clean_users': {
        'task': 'book.tasks.history_update',
        'schedule': crontab(minute=5, hour='*/3'),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static_content', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'static_content', 'media')

AUTH_USER_MODEL = 'account.User'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.outbox'
else:
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# https://django-registration.readthedocs.io/en/3.1/settings.html#django.conf.settings.REGISTRATION_OPEN
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window
REGISTRATION_OPEN = True
REGISTRATION_SALT = os.environ['REGISTRATION_SALT']

LOGIN_REDIRECT_URL = reverse_lazy('account:profile_overall')
LOGOUT_REDIRECT_URL = reverse_lazy('pages:index')
LOGIN_URL = reverse_lazy('login')

DOMAIN = os.environ['DOMAIN']
# CUSTOM SETTINGS
#####################################################
TESTS_IN_PROGRESS = 'pytest' in os.path.basename(sys.argv[0]) or \
                    'py.test' in os.path.basename(sys.argv[0]) or \
                    'test' in sys.argv[1:] or \
                    'jenkins' in sys.argv[1:] or \
                    os.environ.get('CI')

if DEBUG:
    # debug tool_bar
    DEBUG_TOOLBAR_PATCH_SETTINGS = True
    INTERNAL_IPS = ['127.0.0.1']

    # tricks to have debug toolbar when developing with docker
    ip = socket.gethostbyname(socket.gethostname())
    ip = '.'.join(ip.split('.')[:-1])
    ip = f'{ip}.1'
    INTERNAL_IPS.append(ip)

    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ADMINS = (
    ('dmytro.kaminskyi92@gmail.com', 'dmytro.kaminskyi92@gmail.com'),
)

# API
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer', 'JWT', ),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', ),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CORS_ORIGIN_ALLOW_ALL = True

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        },
        'JWT': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        },
    },
}


if TESTS_IN_PROGRESS:
    from settings.settings_tests import *  # noqa

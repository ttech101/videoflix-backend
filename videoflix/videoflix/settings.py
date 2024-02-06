"""
Django settings for videoflix project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-(snwa47!t1=ak__*^%=ue&e%(2bp$kpd5mh8_%a83jz@trwgc-'
SECRET_KEY = 'N(!ynBBNHqm|k+zo"?9>C~sg:)1ndNRp^o0.{-5w?NC6ZBpoM~-OiFEY%0u;MG'







# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['videoflix-backend.tech-mail.eu','videoflix.tech-mail.eu','127.0.0.1','.tech-mail.eu']
CORS_ALLOWED_ORIGINS = [
    "https://videoflix.tech-mail.eu",
    "https://videoflix-backend.tech-mail.eu",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]



CORS_ORIGIN_ALLOW_ALL = False
#CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    "django_rq",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'rest_framework',
    'account',
    'storage.apps.StorageConfig',
    'corsheaders',
    "debug_toolbar",

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'videoflix.middleware.AuthRequiredMiddleware'
]

INTERNAL_IPS = [
    "127.0.0.1",
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
             "REDIS_CLIENT_KWARGS": {
                "ssl_cert_reqs": None,
                "ssl": True,
                },
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
        "KEY_PREFIX": "videoflix"
        }
    }

ROOT_URLCONF = 'videoflix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'videoflix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../../static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
	'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

DEFAULT_FROM_EMAIL = 'Videoflix Support'
SERVER_EMAIL = 'admin@tech-mail.eu'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ttechnomeister@gmail.com'
EMAIL_HOST_PASSWORD = 'edmsbzmeaelkpphh'

FRONTEND_URL = 'https://videoflix.tech-mail.eu'
LOGIN_URL = 'https://videoflix.tech-mail.eu/login/'


IMAGE_MAX_SIZE = 5 * 1024 * 1024  # 5 MB
VIDEO_MAX_SIZE = 50 * 1024 * 1024  # 50 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10

FILE_UPLOAD_MAX_SIZE = {
    'image': IMAGE_MAX_SIZE,
    'video': VIDEO_MAX_SIZE,
}


RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        # 'USERNAME': 'some-user',
#        'PASSWORD': 'foobared',
        'DEFAULT_TIMEOUT': 360,
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
#SESSION_COOKIE_HTTPONLY = True


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE=True

#SECURE_SSL_REDIRECT=True
# CSRF_COOKIE_HTTPONLY = True
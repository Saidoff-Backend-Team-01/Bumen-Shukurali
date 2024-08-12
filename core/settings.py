"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
import os
from .jazzmin_settings import JAZZMIN_SETTINGS
from .ckeditor_settings import CKEDITOR_5_CONFIGS
from datetime import timedelta




load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG'))

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')]


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis', # gis
]



LOCAL_APPS = [
    'common',
    'company',
    'news',
    'subject',
    'account',
]


LIBS = [
    'jazzmin',
    'rest_framework',
    'modeltranslation',
    'django_ckeditor_5',
    'phonenumber_field',
    'leaflet',
    'geoip2',
    'drf_yasg',
    'celery',
    'django_celery_beat',  
    'django_celery_results',  
]


INSTALLED_APPS = LIBS + DJANGO_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russion')),
    ('uz', _('Uzbek')),

)


LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]


ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


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

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'uz', 'ru')

MODELTRANSLATION_TRANSLATION_FILES = (
    'news.translation',
)


MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')




AUTH_USER_MODEL = 'account.User'

JAZZMIN_SETTINGS = JAZZMIN_SETTINGS


CELERY_BROKER_URL = os.getenv('REDIS_LOCATION_CELERY')
CELERY_RESULT_BACKEND = os.getenv('REDIS_LOCATION_CELERY')


CKEDITOR_5_CONFIGS = CKEDITOR_5_CONFIGS


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_LOCATION_CACHE')
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
}


GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
GOOGLE_GRANT_TYPE = os.getenv('GOOGLE_GRANT_TYPE')
SOCIAL_USER_PASSWORD = os.getenv('SOCIAL_USER_PASSWORD')
"""
Django settings for django_server project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
import openai

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "daphne",
    "django_q",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_server",
    "rest_framework",
    "rest_framework.authtoken",
]
ASGI_APPLICATION = "django_server.asgi.application"
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_server.urls"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "django_server.wsgi.application"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "django_server.authentication_classes.permissions.AllowBasedOnMethod"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "django_server.authentication_classes.GoogleAuthBackend.GoogleAuthBackend",
        # "django.contrib.auth.backends.ModelBackend",
        # This is the default that allows us to log in via username for admin
    ],
}

AUTHENTICATION_BACKENDS = [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
    "django_server.authentication_classes.GoogleAuthBackend.GoogleAuthBackend",
    "django.contrib.auth.backends.ModelBackend",  # This is the default that allows us to log in via username for admin
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = ["/app/static/"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ALLOWED_HOSTS = ["*"]
# CSRF_COOKIE_SECURE = False
AUTH_USER_MODEL = "django_server.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
    "LEEWAY": 60,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
    },
}

# settings.py example
Q_CLUSTER = {
    "name": "qcluster",
    "recycle": 500,
    "timeout": 15,
    "queue_limit": 4,
    "cpu_affinity": 1,
    "label": "Django Q",
    "max_attempts": 1,
    "redis": {
        "host": os.environ.get("REDIS_HOST"),
        "port": 6379,
        "db": 0,
    },
}

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": os.environ.get("RDS_DB_USER"),
        "PASSWORD": os.environ.get("RDS_DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": "5432",
    }
}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{os.environ.get('REDIS_HOST')}:6379",
    }
}
SESSION_COOKIE_SECURE = False
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "test3")
openai.api_key = os.environ.get("OPENAI_API_KEY")
CORS_ALLOWED_ORIGINS = [
    "https://chatgpt-forum-fe.vercel.app",
    "http://chatgpt-forum-fe.vercel.app",
]
CSRF_TRUSTED_ORIGINS = [
    "https://chatgpt-forum-fe.vercel.app",
    "http://chatgpt-forum-fe.vercel.app",
    "https://kirillras.net",
]
try:
    from .local_settings import *  # noqa: F401, E402, F403
except ImportError:
    pass

"""
Django settings for django_server project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import openai
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
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
]
ASGI_APPLICATION = "django_server.asgi.application"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "request_logging.middleware.LoggingMiddleware",
    "pyinstrument.middleware.ProfilerMiddleware",
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
        "DIRS": [os.path.join(BASE_DIR, "django_server", "templates")],
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
DEBUG = True
WSGI_APPLICATION = "django_server.wsgi.application"
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "django_server.authentication_classes.permissions.AllowBasedOnMethod"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "django.contrib.auth.backends.ModelBackend",
        # This is the default that allows us to log in via username for admin
    ],
}
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_AUDIENCE = f"https://{AUTH0_DOMAIN}/api/v2/"
AUTH0_ISSUER = f"https://{os.getenv('AUTH0_DOMAIN')}/"
_USERNAME_HANDLER = "django_server.authentication_classes.auth0authorization.jwt_get_username_from_payload_handler"
JWT_AUTH = {
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": _USERNAME_HANDLER,
    "JWT_DECODE_HANDLER": "django_server.authentication_classes.auth0authorization.jwt_decode_token",
    "JWT_ALGORITHM": "RS256",
    "JWT_AUDIENCE": AUTH0_AUDIENCE,
    "JWT_ISSUER": AUTH0_ISSUER,
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
}
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.RemoteUserBackend",
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

AUTH_USER_MODEL = "django_server.User"

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#     },
#     "loggers": {
#         "django": {"handlers": ["console"], "level": "INFO"},
#     },
# }
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",  # change debug level as appropiate
            "propagate": False,
        },
    },
}
# settings.py example
Q_CLUSTER = {
    "name": "DjangoQ2",
    "recycle": 500,
    "timeout": 15,
    "queue_limit": 4,
    "cpu_affinity": 1,
    "label": "Django Q",
    "max_attempts": 1,
    "sqs": {
        "aws_region": "eu-west-1",
        "aws_access_key_id": "AKIAQUAU5PEGFNONBL2J",
        "aws_secret_access_key": os.getenv("SQS_ACCESS_SECRET", "secret"),
    },
}

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
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
SESSION_COOKIE_SECURE = True
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "test3")
openai.api_key = os.getenv("OPENAI_API_KEY")
CORS_ALLOWED_ORIGINS = [
    "https://chatgpt-forum-fe.vercel.app",
    "http://chatgpt-forum-fe.vercel.app",
    "https://www.geppetaboard.com",
    "https://kirillras.net",
]
CSRF_TRUSTED_ORIGINS = [
    "https://chatgpt-forum-fe.vercel.app",
    "http://chatgpt-forum-fe.vercel.app",
    "https://kirillras.net",
    "https://www.geppetaboard.com",
]
CORS_ALLOW_CREDENTIALS = True
# ALLOWED_HOSTS = ["https://www.geppetaboard.com", "127.0.0.1", "localhost"]
ALLOWED_HOSTS = ["*"]
SITE_ID = 1

try:
    from .local_settings import *  # noqa: F401, E402, F403
except ImportError:
    pass

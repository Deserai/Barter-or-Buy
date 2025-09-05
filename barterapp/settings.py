"""
Django settings for barterapp project on Render.
Ready-to-deploy configuration with PostgreSQL and Whitenoise.
"""

import os
from pathlib import Path
import dj_database_url
import environ
import sys

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
env = environ.Env()
env_file = os.path.join(BASE_DIR,".env")
if env_file:
    env.read_env(env_file)

# SECURITY
SECRET_KEY = os.environ.get("SECRET_KEY", "your-local-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS=['127.0.0.1', 'localhost', 'barter-or-buy.onrender.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "barterapp.urls"

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

WSGI_APPLICATION = "barterapp.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default = os.environ.get("DATABASE_URL"),
            conn_max_age = 600, 
            ssl_require=True
            )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login redirects
LOGIN_REDIRECT_URL = "/inbox/"
LOGOUT_REDIRECT_URL = "/login/"

# Allow Render's proxy header for HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTPS_X_FORWARDED_PROTO", "https")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]  # Your local static folder
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/inbox/'

LOGOUT_REDIRECT_URL = '/login/'

LOGGING = {
    'version': 1,
    'disable_exsiting_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'feature_usage.log',
        },
    },
    'loggers':{
        'django':{
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'feature_usage': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

print("DJANGO STARTUP OK", file=sys.stderr)
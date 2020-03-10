""" Configuración de Django 3.0.3 para el proyecto de django template.
"""

import environ

import os

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2

APPS_DIR = BASE_DIR.path("apps")

SECRET_KEY = env("DJANGO_SECRET_KEY", default="3w_%03ttrp$%(kntl6*(q&j3t05!#1ldvu$-dxti&dz_zzm7h+")

DEBUG = env.bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

# Application definition

def get_apps_config(apps):
    apps_config = []
    for app in apps:
        app_dir = APPS_DIR.path(app)
        if os.path.exists(app_dir):
            apps_config.append("apps.%s" % app)
    return apps_config

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = []

LOCAL_APPS = []

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + get_apps_config(LOCAL_APPS)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES_DIRS = []

for app in LOCAL_APPS:
    app_dir = APPS_DIR.path(app).path("templates")
    if os.path.exists(app_dir):
        TEMPLATES_DIRS.push(app_dir)


TEMPLATES_CONTEXT_PROCESSORS = [
    "django.template.context_processors.debug",
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATES_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": TEMPLATES_CONTEXT_PROCESSORS,
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {"default": env.db("DJANGO_DATABASE_URL")}

DATABASES['default']['ATOMIC_REQUESTS'] = True

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

PASSWORD_VALIDATORS = [
    "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    "django.contrib.auth.password_validation.MinimumLengthValidator",
    "django.contrib.auth.password_validation.CommonPasswordValidator",
    "django.contrib.auth.password_validation.NumericPasswordValidator",
]

AUTH_PASSWORD_VALIDATORS = []

for i in PASSWORD_VALIDATORS:
    AUTH_PASSWORD_VALIDATORS.append({"NAME": i})

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "es-CO"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "details": {
            "format": "[%(asctime)s: %(levelname)s] %(pathname)s, linea %(lineno)d: %(message)s"
        }
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "formatter": "details",
            "class": "logging.StreamHandler",
        },
        "logger": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filters": ["require_debug_false"],
            "formatter": "details",
            "filename": "/logs/logger.log",
            "maxBytes": 15744000,  # 15MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["logger", "console"], "propagate": True}
    },
}

# Cache

REDIS_URL = env("DJANGO_REDIS_URL", default="redis:6379")

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"DB": 1, "PARSER_CLASS": "redis.connection.HiredisParser"},
        "TIMEOUT": 3600,
    }
}
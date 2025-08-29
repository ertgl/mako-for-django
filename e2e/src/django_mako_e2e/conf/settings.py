"""
Django settings for django-mako-e2e project.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/

For the deployment checklist, see
https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
"""

from pathlib import Path


CONF_DIR = Path(__file__).resolve().parent

PACKAGE_DIR = CONF_DIR.parent

SRC_DIR = PACKAGE_DIR.parent

PROJECT_DIR = SRC_DIR.parent

BASE_DIR = PROJECT_DIR

MAKO_DIR = PACKAGE_DIR / "mako"

TEMPLATES_DIR = PACKAGE_DIR / "templates"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--kl7@v&zmq2fzmraxgx2jeabnm$7z*kf!al0gjgf8%@0$iwi#r"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_mako_e2e.modules.samples",
]


ALLOWED_HOSTS: list[str] = []

ROOT_URLCONF = "django_mako_e2e.conf.urls"

ASGI_APPLICATION = "django_mako_e2e.inet.entrypoints.asgi.application"

WSGI_APPLICATION = "django_mako_e2e.inet.entrypoints.wsgi.application"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SHARED_TEMPLATE_CONTEXT_PROCESSORS = [
    "django.template.context_processors.debug",
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.tz",
    "django.template.context_processors.i18n",
    "django.contrib.messages.context_processors.messages",
    "django.template.context_processors.static",
    "django.template.context_processors.media",
]

MAKO_TEMPLATE_CONTEXT_PROCESSORS = [
    "django_mako.template.context_processors.url",
]

MAKO_TEMPLATE_OPTIONS = {
    "encoding_errors": "strict" if DEBUG else "htmlentityreplace",
}

TEMPLATES = [
    {
        "BACKEND": "django_mako.MakoEngine",
        "DIRS": [
            MAKO_DIR,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                *SHARED_TEMPLATE_CONTEXT_PROCESSORS,
                *MAKO_TEMPLATE_CONTEXT_PROCESSORS,
            ],
            "template": {
                **MAKO_TEMPLATE_OPTIONS,
            },
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            TEMPLATES_DIR,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                *SHARED_TEMPLATE_CONTEXT_PROCESSORS,
            ],
        },
    },
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "file::memory:",
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

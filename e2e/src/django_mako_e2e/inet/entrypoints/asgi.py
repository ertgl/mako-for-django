"""
ASGI config for django-mako-e2e project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

__all__ = ["application"]

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "django_mako_e2e.conf.settings",
)

application = get_asgi_application()

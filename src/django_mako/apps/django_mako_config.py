__all__ = ["DjangoMakoConfig"]

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoMakoConfig(AppConfig):
    name = "django_mako"
    verbose_name = _("Mako Template Engine")

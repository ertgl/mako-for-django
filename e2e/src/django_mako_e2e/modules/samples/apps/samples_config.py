__all__ = ["SamplesConfig"]

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SamplesConfig(AppConfig):
    label = "samples"
    name = "django_mako_e2e.modules.samples"
    verbose_name = _("Samples")

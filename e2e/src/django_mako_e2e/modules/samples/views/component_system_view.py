__all__ = ["ComponentSystemView"]

from clsx import clsx
from django.views.generic import TemplateView


class ComponentSystemView(TemplateView):
    template_name = "/samples/views/component-system.html.mako"

    extra_context = {  # ruff:ignore[mutable-class-default]
        "clsx": clsx,
    }

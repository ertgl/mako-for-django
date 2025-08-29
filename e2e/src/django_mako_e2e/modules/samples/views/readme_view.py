__all__ = ["ReadmeView"]

from clsx import clsx
from django.views.generic import TemplateView


class ReadmeView(TemplateView):
    template_name = "/samples/views/readme.html.mako"

    extra_context = {
        "clsx": clsx,
    }

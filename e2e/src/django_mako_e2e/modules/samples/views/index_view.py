__all__ = ["IndexView"]

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "/samples/views/index.html.mako"

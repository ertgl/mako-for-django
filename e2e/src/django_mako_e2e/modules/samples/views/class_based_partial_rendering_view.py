__all__ = ["ClassBasedPartialRenderingView"]

from django.views.generic import TemplateView


class ClassBasedPartialRenderingView(TemplateView):
    template_name = "/samples/views/partial-rendering.html.mako"

    extra_context = {
        "partial_template_uri": "/samples/partial/class-based.html.mako",
    }

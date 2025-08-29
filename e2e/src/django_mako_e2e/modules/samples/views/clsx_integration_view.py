__all__ = ["CLSXIntegrationView"]

from dataclasses import (
    dataclass,
    field,
)

from clsx import clsx
from django.views.generic import TemplateView


@dataclass()
class Post:
    title: str = field(
        default="",
        kw_only=True,
    )

    body: str = field(
        default="",
        kw_only=True,
    )


posts = [Post(title=f"Post {i + 1}") for i in range(10)]


class CLSXIntegrationView(TemplateView):
    template_name = "/samples/views/clsx-integration.html.mako"

    extra_context = {
        "clsx": clsx,
        "posts": posts,
    }

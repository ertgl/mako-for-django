__all__ = ["FunctionalPartialRenderingView"]

from typing import Callable

from django.http import (
    HttpRequest,
    HttpResponseBase,
)
from django.shortcuts import render


class FunctionalPartialRenderingView:
    @staticmethod
    def index_view(
        request: HttpRequest,
    ) -> HttpResponseBase:
        return render(
            request,
            "/samples/views/partial-rendering.html.mako",
            context={
                "partial_template_uri": "/samples/partial/functional.html.mako",
            },
        )

    @classmethod
    def as_view(cls) -> Callable[[HttpRequest], HttpResponseBase]:
        return cls.index_view

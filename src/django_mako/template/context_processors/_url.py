__all__ = ["url"]

from typing import Any

from django.http import HttpRequest
from django.urls import (
    reverse,
    reverse_lazy,
)


def url(
    request: HttpRequest,
) -> dict[str, Any]:
    return {
        "reverse_url": reverse,
        "reverse_url_lazy": reverse_lazy,
    }

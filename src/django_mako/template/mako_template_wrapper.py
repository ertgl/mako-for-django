__all__ = ["MakoTemplateWrapper"]

from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    cast,
)

from django.http import HttpRequest
from django.template.backends.utils import (
    csrf_input_lazy,
    csrf_token_lazy,
)
from mako.template import Template

from django_mako.template.backend.exception import MakoExceptionHandler
from django_mako.template.mako_template_origin import MakoTemplateOrigin


if TYPE_CHECKING:
    from django_mako.template.backend.engine.mako_engine import MakoEngine


class MakoTemplateWrapper:
    template: Template

    def __init__(
        self,
        template: Template,
    ) -> None:
        self.template = template

    @cached_property
    def origin(self) -> MakoTemplateOrigin:
        return MakoTemplateOrigin.from_template(self.template)

    def render(
        self,
        context: dict[str, Any] | None = None,
        request: HttpRequest | None = None,
    ) -> str:
        if context is None:
            context = {}

        backend = cast(
            Optional["MakoEngine"],
            getattr(self.template, "backend", None),
        )

        if request is not None:
            context["request"] = request
            context["csrf_input"] = csrf_input_lazy(request)
            context["csrf_token"] = csrf_token_lazy(request)

            if backend is not None:
                for generate_context in backend.template_context_processors:
                    context.update(generate_context(request))

        with MakoExceptionHandler(
            backend=backend,
            template=self.template,
            uri=self.template.uri,
        ):
            return self.template.render_unicode(  # type: ignore[no-any-return]
                **context,
            )

__all__ = ["MakoExceptionHandler"]

from contextlib import ContextDecorator
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Optional,
    cast,
)

from django.template import (
    Origin,
    TemplateDoesNotExist,
    TemplateSyntaxError,
)
from mako.exceptions import TopLevelLookupException
from mako.template import Template

from django_mako.template.backend.debugging import MakoExceptionInfo
from django_mako.template.backend.exception.lookup_exception_types import (
    LOOKUP_EXCEPTION_TYPES,
)
from django_mako.template.backend.exception.positional_exception_types import (
    POSITIONAL_EXCEPTION_TYPES,
)
from django_mako.template.mako_template_origin import MakoTemplateOrigin


if TYPE_CHECKING:
    from django_mako.template.backend.engine.mako_engine import MakoEngine


class MakoExceptionHandler(
    ContextDecorator,
):
    backend: Optional["MakoEngine"]

    template: Template | None

    uri: str | None

    @staticmethod
    def maybe_convert(
        exception: BaseException,
        backend: Optional["MakoEngine"] = None,
        template: Template | None = None,
        uri: str | None = None,
    ) -> BaseException:
        if not uri and template:
            uri = template.uri
        if isinstance(exception, POSITIONAL_EXCEPTION_TYPES):
            template_syntax_error = TemplateSyntaxError(
                exception.args[0],
            ).with_traceback(
                exception.__traceback__,
            )
            MakoExceptionInfo.set_for_exception(
                template_syntax_error,
                exception,
                backend=backend,
                template=template,
                uri=uri,
            )
            return template_syntax_error
        elif isinstance(exception, LOOKUP_EXCEPTION_TYPES):
            tried: list[tuple[MakoTemplateOrigin, str]] = []
            if (
                backend is not None
                and uri is not None
                and isinstance(exception, TopLevelLookupException)
            ):
                for filename in backend.iter_template_filenames(uri):
                    tried.append(
                        (
                            MakoTemplateOrigin(
                                filename,
                                backend=backend,
                                template_name=uri,
                            ),
                            "Source does not exist",
                        ),
                    )
            template_lookup_exception = TemplateDoesNotExist(
                exception.args[0],
                backend=backend,
                tried=cast(list[tuple[Origin, str]], tried),
            ).with_traceback(
                exception.__traceback__,
            )
            MakoExceptionInfo.set_for_exception(
                template_lookup_exception,
                exception,
                backend=backend,
                template=template,
                uri=uri,
            )
            return template_lookup_exception
        MakoExceptionInfo.set_for_exception(
            exception,
            exception,
            backend=backend,
            template=template,
            uri=uri,
        )
        return exception

    def __init__(
        self,
        backend: Optional["MakoEngine"] = None,
        template: Template | None = None,
        uri: str | None = None,
    ) -> None:
        self.backend = backend
        self.template = template
        self.uri = uri

    def __enter__[C: "MakoExceptionHandler"](self: C) -> C:
        return self

    def __exit__(
        self,
        exception_type: Optional[type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if exception is None:
            return
        new_exception = self.maybe_convert(
            exception,
            backend=self.backend,
            template=self.template,
            uri=self.uri,
        )
        if new_exception is exception:
            raise new_exception
        raise new_exception from exception

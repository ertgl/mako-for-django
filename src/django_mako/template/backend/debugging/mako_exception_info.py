__all__ = ["MakoExceptionInfo"]

from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

from mako.exceptions import (
    CompileException,
    RichTraceback,
    SyntaxException,
)
from mako.template import Template

from django_mako.template.backend.exception.positional_exception_types import (
    POSITIONAL_EXCEPTION_TYPES,
)


if TYPE_CHECKING:
    from django_mako.template.backend.engine.mako_engine import MakoEngine


class MakoExceptionInfo:
    @staticmethod
    def from_exception(
        exception: BaseException,
        backend: Optional["MakoEngine"] = None,
        template: Template | None = None,
        uri: str | None = None,
    ) -> dict[str, Any]:
        if isinstance(exception, POSITIONAL_EXCEPTION_TYPES):
            return MakoExceptionInfo.from_positional_exception(
                exception,
                backend=backend,
                template=template,
                uri=uri,
            )
        return MakoExceptionInfo.from_traceback(
            exception,
            backend=backend,
            template=template,
            uri=uri,
        )

    @staticmethod
    def from_positional_exception(
        exception: CompileException | SyntaxException,
        backend: Optional["MakoEngine"] = None,
        template: Template | None = None,
        uri: str | None = None,
    ) -> dict[str, Any]:
        context_lines = 10
        lineno = exception.lineno
        source = exception.source

        if source is None:
            exception_file_path = Path(exception.filename)
            if exception_file_path.exists():
                source = exception_file_path.read_text()

        if source is not None:
            lines = list(enumerate(source.split("\n"), start=1))
            during = lines[lineno - 1][1]
            total = len(lines)
            top = max(0, lineno - context_lines - 1)
            bottom = min(total, lineno + context_lines)
        else:
            during = ""
            lines = []
            total = top = bottom = 0

        return {
            "name": exception.filename,
            "message": exception.args[0],
            "source_lines": lines[top:bottom],
            "line": lineno,
            "before": "",
            "during": during,
            "after": "",
            "total": total,
            "top": top,
            "bottom": bottom,
        }

    @staticmethod
    def from_traceback(
        exception: BaseException,
        backend: Optional["MakoEngine"] = None,
        template: Template | None = None,
        uri: str | None = None,
    ) -> dict[str, Any]:
        traceback = RichTraceback(
            error=exception,
        )

        if len(traceback.records) == 0:
            return {
                "message": exception.args[0],
            }

        template_frame = MakoExceptionInfo.get_errored_template_frame(traceback)

        frame: tuple[Any, Any, Any]

        if template_frame is not None:
            frame = (
                template_frame[0],
                template_frame[1],
                template_frame[3],
            )
        else:
            stack_frame = traceback.traceback[0]
            frame = (
                stack_frame[0],
                stack_frame[1],
                getattr(exception, "source", None),
            )

        (
            filename,
            lineno,
            source,
        ) = frame

        context_lines = 10

        if source is None:
            exception_file_path = Path(filename)
            if exception_file_path.exists():
                source = exception_file_path.read_text()

        if source:
            lines = list(enumerate(source.split("\n"), start=1))
            during = lines[lineno - 1][1] if lineno < len(lines) else ""
            total = len(lines)
            top = max(0, lineno - context_lines - 1)
            bottom = min(total, lineno + context_lines)
        else:
            during = ""
            lines = []
            total = top = bottom = 0

        return {
            "name": filename,
            "message": exception.args[0],
            "source_lines": lines[top:bottom],
            "line": lineno,
            "before": "",
            "during": during,
            "after": "",
            "total": total,
            "top": top,
            "bottom": bottom,
        }

    @staticmethod
    def set_for_exception(
        new_exception: BaseException,
        exception: BaseException,
        backend: Optional["MakoEngine"] = None,
        template: Template | None = None,
        uri: str | None = None,
    ) -> None:
        new_exception.template_debug = (  # type: ignore[attr-defined]
            MakoExceptionInfo.from_exception(
                exception,
                backend=backend,
                template=template,
                uri=uri,
            )
        )

    @staticmethod
    def get_errored_template_frame(
        traceback: RichTraceback,
    ) -> tuple[Any, Any, Any, Any] | None:
        for frame in traceback.records[::-1]:
            (
                filename,
                lineno,
                function,
                line,
                template_filename,
                template_lineno,
                template_line,
                template_source,
            ) = frame
            if template_filename or template_source:
                return (
                    template_filename,
                    template_lineno,
                    template_line,
                    template_source,
                )
        return None

__all__ = ["MakoEngine"]

from functools import cached_property
from typing import (
    Any,
    Callable,
)

from django.conf import settings
from django.http import HttpRequest
from django.template.backends.base import BaseEngine
from django.utils.module_loading import import_string
from mako.lookup import TemplateLookup
from mako.template import Template

from django_mako.template import (
    MakoTemplateOrigin,
    MakoTemplateWrapper,
)
from django_mako.template.backend.exception import (
    MakoExceptionHandler,
)


class MakoEngine(
    BaseEngine,
):
    lookup_directory_name: str

    lookup: TemplateLookup

    context_processors: list[str]

    template_options: dict[str, Any]

    def __init__(
        self,
        params: dict[str, Any],
    ) -> None:
        params = params.copy()

        options = params.pop("OPTIONS", {}).copy()

        super(
            MakoEngine,
            self,
        ).__init__(
            params,
        )

        self.context_processors = options.pop("context_processors", [])

        self.directory_name = options.get("directory_name") or "mako"

        self.template_options = options.get("template", {})

        lookup_options = options.get("lookup", {})
        lookup_options.setdefault("directories", self.template_dirs)
        lookup_options.setdefault("filesystem_checks", settings.DEBUG)
        lookup_options.setdefault("input_encoding", "utf-8")
        lookup_options.setdefault("output_encoding", "utf-8")

        self.lookup = TemplateLookup(
            **{
                **self.template_options,
                **lookup_options,
            },
        )

    @property
    def app_dirname(self) -> str:
        return self.directory_name

    @cached_property
    def template_context_processors(
        self,
    ) -> list[Callable[[HttpRequest], dict[str, Any]]]:
        return [import_string(path) for path in self.context_processors]

    def from_string(
        self,
        template_code: str,
    ) -> MakoTemplateWrapper:
        with MakoExceptionHandler(
            backend=self,
        ):
            template = Template(
                **self.template_options,
                text=template_code,
                lookup=self.lookup,
            )
            self.prepare_template(template)
            return MakoTemplateWrapper(template)

    def get_template(
        self,
        template_name: str,
    ) -> MakoTemplateWrapper:
        with MakoExceptionHandler(
            backend=self,
            uri=template_name,
        ):
            template = self.lookup.get_template(
                template_name,
            )
            self.prepare_template(template)
            return MakoTemplateWrapper(template)

    def prepare_template(
        self,
        template: Template,
    ) -> None:
        setattr(
            template,
            "backend",
            self,
        )
        setattr(
            template,
            "origin",
            MakoTemplateOrigin.from_template(template),
        )

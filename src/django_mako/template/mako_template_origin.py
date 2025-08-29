__all__ = ["MakoTemplateOrigin"]

from typing import (
    TYPE_CHECKING,
    Optional,
)

from django.template.base import UNKNOWN_SOURCE
from mako.lookup import TemplateLookup
from mako.template import Template


if TYPE_CHECKING:
    from django_mako.template.backend.engine.mako_engine import MakoEngine


class MakoTemplateOrigin:
    backend: Optional["MakoEngine"]

    name: str

    template_name: str | None

    @classmethod
    def from_template[C: "MakoTemplateOrigin"](
        cls: type[C],
        template: Template,
    ) -> C:
        return cls(
            template.filename,
            backend=template.backend,
            template_name=template.uri,
        )

    def __init__(
        self,
        name: str | None,
        backend: Optional["MakoEngine"] = None,
        template_name: str | None = None,
    ) -> None:
        self.name = name or UNKNOWN_SOURCE
        self.backend = backend
        self.template_name = template_name

    @property
    def lookup(self) -> TemplateLookup:
        return self.backend.lookup if self.backend else None

    @property
    def loader_name(self) -> str:
        if not self.lookup:
            return "<unknown loader>"
        return f"{self.lookup.__class__.__module__}.{self.lookup.__class__.__name__}"

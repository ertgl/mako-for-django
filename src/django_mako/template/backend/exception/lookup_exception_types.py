__all__ = ["LOOKUP_EXCEPTION_TYPES"]

from mako.exceptions import TemplateLookupException


LOOKUP_EXCEPTION_TYPES = (
    FileNotFoundError,
    TemplateLookupException,
)

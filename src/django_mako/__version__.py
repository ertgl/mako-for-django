__all__ = [
    "VERSION_INFO",
    "__version__",
]

from typing import cast


__version__ = "1.0.0"

VERSION_INFO = cast(
    tuple[int, int, int],
    tuple(map(int, __version__.split("."))),
)

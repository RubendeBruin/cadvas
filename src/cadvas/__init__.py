"""This module initializes the `cadvas` package and sets up its environment."""

import os
from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

from .elements import Box, CadItem, Circle, Measure, Polygon, Segment
from .widget import QCadvasWidget

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

os.environ["PYQTGRAPH_QT_LIB"] = "PySide6"

__all__ = [
    "Box",
    "CadItem",
    "Circle",
    "Measure",
    "Polygon",
    "QCadvasWidget",
    "Segment",
]

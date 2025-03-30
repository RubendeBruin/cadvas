import sys
import os

from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

os.environ['PYQTGRAPH_QT_LIB'] = 'PySide6'

from .widget import QCadvasWidget
from .elements import CadItem, Segment, Box, Circle, Polygon, Measure

__all__ = [
    "QCadvasWidget", 
    "CadItem", 
    "Segment", 
    "Box", 
    "Circle", 
    "Polygon", 
    "Measure",
]
                    


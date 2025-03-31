"""This module defines the `QCadvasWidget` class.

This is a custom widget based on `pyqtgraph.GraphicsLayoutWidget` for managing and displaying CAD-like items.

Classes:
    QCadvasWidget: A widget that provides a graphical layout with a view box
                   for rendering and managing CAD items.
Dependencies:
    - pyqtgraph
    - CadItem (from .elements)
Usage:
    The `QCadvasWidget` class can be used to create a graphical interface
    for displaying and interacting with CAD items. It provides methods for
    adding, updating, and clearing items within the view box.

Example:
    widget = QCadvasWidget()
    cad_item = CadItem(...)
    widget.addCadItem(cad_item)
    widget.clearDrawing()
"""

import pyqtgraph as pg

from .elements import CadItem


class QCadvasWidget(pg.GraphicsLayoutWidget):
    """QCadvasWidget is a custom widget that extends `pg.GraphicsLayoutWidget`.

    QCadvasWidget is used to provide a specialized interface for managing and displaying CAD-like items within a
    PyQtGraph view box.

    Methods:
        __init__(*args, **kwargs):
            Initializes the widget with a specified background color, layout, and view box.
        updateMeasurements():
            Updates the measurements of all items in the widget by calling their `updateItems` method
            with the current view box.
        addCadItem(item: CadItem, do_bounds=True):
            Adds a CAD item to the widget, creates its graphical representation in the view box,
            and optionally adjusts its bounds.
        clearDrawing():
            Clears all CAD items from the widget and removes their graphical representations from the view box.
    """

    def __init__(self, *args, **kwargs):
        """Initializes the widget with a specified background color, layout, and view box.

        Args:
            *args: Variable length argument list passed to the parent class initializer.
            **kwargs: Arbitrary keyword arguments passed to the parent class initializer.

        Attributes:
            w (ViewBox): The view box added to the layout, with aspect ratio locked and auto-range disabled.
            _items (list): A list to store items associated with the widget.

        Notes:
            - The background color is set to (254, 254, 254).
            - The `sigRangeChanged` signal of the view box is connected to the `updateMeasurements` method.
        """
        super().__init__(*args, **kwargs)
        self.setBackground((254, 254, 254))

        sub1 = self.addLayout()
        w = sub1.addViewBox()

        w.setAspectLocked(True)
        w.enableAutoRange(False)

        self._items = []

        w.sigRangeChanged.connect(self.updateMeasurements)

        self.w = w

    def updateMeasurements(self):
        """Updates the measurements of all items in the widget.

        Iterates through the list of items (`self._items`) and calls the `updateItems` method on each item,
        passing the widget's width (`self.w`) as a parameter.
        """
        for p in self._items:
            p.updateItems(self.w)

    def addCadItem(self, item: CadItem, do_bounds=True):
        """Adds a CAD item to the widget.

        Args:
            item (CadItem): The CAD item to be added to the widget.
            do_bounds (bool): If True, adjusts the bounds of the item in the view box.
        """
        item.createItems(self.w, do_bounds)
        self._items.append(item)

    def clearDrawing(self):
        """Clears all CAD items from the widget."""
        self._items = []
        self.w.clear()

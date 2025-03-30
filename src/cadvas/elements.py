"""This module defines various CAD elements that can be drawn on a `pg.PlotWidget` using PyQtGraph and PySide6.

In this package, each element is represented as a class inheriting from the abstract base class `CadItem`.

Classes:
    - CadItem: Abstract base class for all CAD elements. Defines the interface for creating and updating items.
    - Segment: Represents a line segment between two points.
    - Box: Represents a:1
rectangular box defined by its lower-left and upper-right corners.
    - Polygon: Represents a closed polygon defined by a list of points.
    - Circle: Represents a circle defined by its center and radius.
    - Measure: Represents a measurement line with optional offset and distance annotation.
Constants:
    - MEASURE_COLOR: Default color for measurement lines and text.
Usage:
    Each CAD element class provides methods to create and update graphical items on a `pg.PlotWidget`.
    These items can be used to visualize geometric shapes and measurements in a PyQtGraph-based application.

Classes and Methods:
    - CadItem:
        - createItems(target: pg.PlotWidget, do_bounds: bool): Abstract method to create and add items to the target widget.
        - updateItems(target: pg.PlotWidget): Abstract method to update items on the target widget.
        - in_view(x: float, y: float, w: pg.PlotWidget): Checks if a point is within the view range of the widget.
    - Segment:
        - __init__(start: tuple, end: tuple): Initializes a line segment with start and end points.
        - createItems(target: pg.PlotWidget, do_bounds: bool): Creates and adds a line segment to the target widget.
        - updateItems(target: pg.PlotWidget): Updates the line segment (not implemented).
    - Box:
        - __init__(lower_left: tuple, upper_right: tuple): Initializes a rectangle with lower-left and upper-right corners.
        - createItems(target: pg.PlotWidget, do_bounds: bool): Creates and adds a rectangle to the target widget.
        - updateItems(target: pg.PlotWidget): Updates the rectangle (not implemented).
    - Polygon:
        - __init__(points: list): Initializes a polygon with a list of points.
        - createItems(target: pg.PlotWidget, do_bounds: bool): Creates and adds a polygon to the target widget.
        - clicked(event): Handles mouse press events on the polygon.
        - updateItems(target: pg.PlotWidget): Updates the polygon (not implemented).
    - Circle:
        - __init__(center: tuple, radius: float): Initializes a circle with a center and radius.
        - createItems(target: pg.PlotWidget, do_bounds: bool): Creates and adds a circle to the target widget.
        - updateItems(target: pg.PlotWidget): Updates the circle (not implemented).
    - Measure:
        - __init__(start: tuple, end: tuple, offset: float): Initializes a measurement line with start and end points, and an optional offset.
        - createItems(target: pg.PlotWidget, do_bounds: bool): Creates and adds a measurement line, arrows, and distance annotation to the target widget.
        - updateItems(target: pg.PlotWidget): Updates the visibility of the measurement line and its components based on the view range.
"""

import logging
import math
from abc import ABC, abstractmethod

import pyqtgraph as pg
from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QBrush, QColor, QPolygonF
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsPolygonItem,
    QGraphicsRectItem,
    QGraphicsSceneMouseEvent,
)

logger = logging.getLogger(__name__)

MEASURE_COLOR = QColor(0, 200, 150)

"""
Use ,ignoreBounds=True to speed-up adding to plot

"""


class CadItem(ABC):
    """CadItem is an abstract base class.

    This class defines the interface for creating and updating graphical items in a plotting widget, as well as
    checking if a point is within the view.

    Methods:
        createItems(target: pg.PlotWidget, do_bounds: bool = False):
            Abstract method to create graphical items and add them to the specified target widget.
            Parameters:
                target (pg.PlotWidget): The plotting widget where items will be added.
                do_bounds (bool): Optional flag to determine if bounds should be considered.
        updateItems(target: pg.PlotWidget):
            Abstract method to update the graphical items in the specified target widget.
            Parameters:
                target (pg.PlotWidget): The plotting widget where items will be updated.
        in_view(x: float, y: float, w: pg.PlotWidget) -> bool:
            Checks if a given point (x, y) is within the visible range of the specified widget.
            Parameters:
                x (float): The x-coordinate of the point.
                y (float): The y-coordinate of the point.
                w (pg.PlotWidget): The plotting widget whose view range is considered.

    Returns:
                bool: True if the point is within the view range, False otherwise.
    """

    @abstractmethod
    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        """Creates items and adds them to target."""
        pass

    @abstractmethod
    def updateItems(self, target: pg.PlotWidget):
        """Updates the items."""
        pass

    def in_view(self, x: float, y: float, w: pg.PlotWidget) -> bool:
        """Determines whether a point (x, y) is within the visible range of a given view.

        Args:
            x (float): The x-coordinate of the point to check.
            y (float): The y-coordinate of the point to check.
            w (object): The view object that provides the visible range via its `viewRect()` method.

        Returns:
            bool: True if the point (x, y) is within the visible range of the view, False otherwise.
        """
        view_range = w.viewRect()
        return bool(view_range.left() <= x <= view_range.right() and view_range.top() <= y <= view_range.bottom())


class Segment(CadItem):
    """Segment is a line between two points."""

    def __init__(self, start, end):
        """Initializes an instance of the class with the specified start and end points.

        Args:
            start: The starting point of the element.
            end: The ending point of the element.
        """
        self.start = start
        self.end = end

    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        """Creates and adds graphical items to the specified PlotWidget.

        This method creates a QGraphicsLineItem representing a line between
        the `start` and `end` points of the object. The line is styled with
        a pen of width 0.1 and added to the provided PlotWidget.

        Args:
            target (pg.PlotWidget): The PlotWidget to which the line item
                will be added.
            do_bounds (bool, optional): If True, the bounds of the line
                item will be considered when adding it to the PlotWidget.
                Defaults to False.

        Returns:
            None
        """
        self.line = QGraphicsLineItem(*self.start, *self.end)
        pen = self.line.pen()
        pen.setWidthF(0.1)
        self.line.setPen(pen)
        target.addItem(self.line, ignoreBounds=not do_bounds)

    def updateItems(self, target: pg.PlotWidget):
        """Updates the items in the specified PlotWidget target.

        This method is intended to modify or refresh the graphical elements
        displayed within the provided PlotWidget.

        Args:
            target (pg.PlotWidget): The PlotWidget instance to update.
        """
        pass


class Box(CadItem):
    """Box is a rectangle."""

    def __init__(self, lower_left, upper_right):
        """Initializes a new instance of the class with the specified lower-left and upper-right coordinates.

        Args:
            lower_left: The coordinates of the lower-left corner.
            upper_right: The coordinates of the upper-right corner.
        """
        self.lower_left = lower_left
        self.upper_right = upper_right

    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        """Creates and adds a rectangular graphical item to the specified PlotWidget.

        This method calculates the width and height of a rectangle based on the
        `upper_right` and `lower_left` coordinates of the object. It then creates
        a `QGraphicsRectItem` representing the rectangle, sets its pen width, and
        adds it to the provided `target` PlotWidget.

        Args:
            target (pg.PlotWidget): The PlotWidget to which the rectangle will be added.
            do_bounds (bool, optional): If True, the rectangle's bounds will be
                considered when adding it to the PlotWidget. Defaults to False.

        Attributes:
            rect (QGraphicsRectItem): The graphical rectangle item created and added
                to the PlotWidget.
        """
        x, y = self.lower_left
        w = self.upper_right[0] - self.lower_left[0]
        h = self.upper_right[1] - self.lower_left[1]

        self.rect = QGraphicsRectItem(QRectF(x, y, w, h))

        pen = self.rect.pen()
        pen.setWidthF(0.1)
        self.rect.setPen(pen)
        target.addItem(self.rect, ignoreBounds=not do_bounds)

    def updateItems(self, target: pg.PlotWidget):
        """Updates the items in the specified PlotWidget target.

        This method is intended to modify or refresh the graphical elements
        displayed in the provided pyqtgraph PlotWidget.

        Args:
            target (pg.PlotWidget): The PlotWidget instance to update.
        """
        pass


class ClickablePolygon(QGraphicsPolygonItem):
    """A QGraphicsPolygonItem subclass that emits a click event."""

    def __init__(self, points, parent=None):
        """Initializes an instance of the class.

        Args:
            points (list of tuple): A list of tuples representing points, where each tuple contains
                coordinates (x, y) of a point.
            parent (QObject, optional): The parent object. Defaults to None.
        """
        super().__init__(QPolygonF([QPointF(*p) for p in points]), parent)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        """Handles the mouse press event by changing the brush color."""
        self.setBrush(QBrush(QColor(0, 254, 0)))
        self.update()
        super().mousePressEvent(event)  # Call parent method to keep default behavior


class Polygon(CadItem):
    """Polygon is a closed segment."""

    def __init__(self, points):
        """Initializes an instance of the class with the given points.

        Args:
            points (iterable): A collection of points to initialize the instance with.
        """
        self.points = points

    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        """Creates graphical items for the given target PlotWidget and adds them to it."""
        self.poly = ClickablePolygon(self.points)  # Use our custom subclass
        target.addItem(self.poly)

    def updateItems(self, target: pg.PlotWidget):
        """Updates the items in the specified PlotWidget target."""
        pass


class Circle(CadItem):
    """Polygon is a closed segment."""

    def __init__(self, center, radius):
        """Initialize a new instance of the class.

        Args:
            center (tuple or list): The coordinates of the center point.
            radius (float): The radius of the element.
        """
        self.center = center
        self.radius = radius

    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        """Creates and adds graphical items to the specified PlotWidget.

        This method creates a circular graphical item (QGraphicsEllipseItem)
        based on the object's center and radius attributes, and adds it to
        the provided PlotWidget. The circle's pen width is set to 0.1.

        Args:
            target (pg.PlotWidget): The PlotWidget to which the graphical
                items will be added.
            do_bounds (bool, optional): If True, the bounds of the circle
                will be considered when adding it to the PlotWidget. Defaults
                to False.

        Attributes:
            circle (QGraphicsEllipseItem): The graphical representation of
                the circle created and added to the PlotWidget.
        """
        self.circle = QGraphicsEllipseItem(
            self.center[0] - self.radius,
            self.center[1] - self.radius,
            2 * self.radius,
            2 * self.radius,
        )
        pen = self.circle.pen()
        pen.setWidthF(0.1)
        self.circle.setPen(pen)
        target.addItem(self.circle, ignoreBounds=not do_bounds)

    def updateItems(self, target: pg.PlotWidget):
        """Updates the items in the given PlotWidget target.

        This method is intended to modify or refresh the graphical elements
        displayed in the specified PlotWidget.

        Args:
            target (pg.PlotWidget): The PlotWidget instance to update.
        """
        pass


class Measure(CadItem):
    """The `Measure` class represents a measurement object defined by a start point, an end point, and an optional perpendicular offset.

    This class provides methods to create and update graphical
    representations of the measurement in a `pg.PlotWidget`.
        start (tuple): The starting point of the measurement as a tuple (x, y).
        end (tuple): The ending point of the measurement as a tuple (x, y).

    Methods:
        __init__(start, end, offset=0):
            Initializes a measurement object with a start point, end point, and optional offset.
            Raises a warning if the distance between start and end points is zero.
        createItems(target: pg.PlotWidget, do_bounds=False):
            Creates and adds graphical items to a target `pg.PlotWidget` for visual representation.
            Generates lines, arrows, and text to represent the measurement.
        updateItems(target: pg.PlotWidget):
            Updates the visibility of graphical items based on their presence within the view
            range of the target `pg.PlotWidget`.
        in_view(x, y, target: pg.PlotWidget) -> bool:
            Determines whether a given point (x, y) is within the view range of the target
            `pg.PlotWidget`.
        Warning: If the distance between the start and end points is zero, a warning is issued
    """

    def __init__(self, start, end, offset=0):
        """Initializes a measurement object with a start point, end point, and optional offset.

        Args:
            start (tuple): A tuple (x, y) representing the starting point of the measurement.
            end (tuple): A tuple (x, y) representing the ending point of the measurement.

            offset (float, optional): A perpendicular offset to apply to the midpoint. Defaults to 0.
                Offset will offset the measurement line to the left side of the endpoint when looking from start to end.

        Attributes:
            start (tuple): The starting point of the measurement.
            end (tuple): The ending point of the measurement.
            distance (float): The Euclidean distance between the start and end points.
            _invalid (bool): Indicates whether the measurement is invalid (e.g., zero length).
            offset (tuple): The calculated offset vector applied to the midpoint.
            midpoint (tuple): The midpoint of the measurement, adjusted by the offset.
            ndx (float): The normalized x-component of the direction vector from start to end.
            ndy (float): The normalized y-component of the direction vector from start to end.
            angle (float): The angle of the measurement in degrees, measured counterclockwise
                           from the positive x-axis.

        Raises:
            Warning: If the distance between start and end points is zero, a warning is issued
                     and the measurement is marked as invalid.
        """
        self.start = start
        self.end = end

        dx = start[0] - end[0]
        dy = start[1] - end[1]
        self.distance = math.sqrt(dx**2 + dy**2)

        if self.distance == 0:
            logger.warning("Can not create a measurement with length 0")
            self._invalid = True
            return

        self._invalid = False

        ndx = dx / self.distance
        ndy = dy / self.distance

        self.offset = (-offset * ndy, offset * ndx)

        self.midpoint = (
            0.5 * (start[0] + end[0]) + self.offset[0],
            0.5 * (start[1] + end[1]) + self.offset[1],
        )

        self.ndx = ndx
        self.ndy = ndy

        self.angle = math.degrees(math.atan2(dy, dx))

    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        """Creates and adds graphical items to a target PlotWidget for visual representation.

        This method generates various graphical elements such as lines, arrows, and text
        to represent measurements or annotations. The items are positioned and styled
        based on the object's attributes and added to the specified target PlotWidget.

        Args:
            target (pg.PlotWidget): The PlotWidget to which the graphical items will be added.
            do_bounds (bool, optional): If True, the bounds of the items will be considered
                when adding them to the target. Defaults to False.

        Returns:
            None
        """
        if self._invalid:
            return

        self.line = QGraphicsLineItem(
            self.start[0] + self.offset[0],
            self.start[1] + self.offset[1],
            self.end[0] + self.offset[0],
            self.end[1] + self.offset[1],
        )
        pen = self.line.pen()
        pen.setWidthF(0.1)
        pen.setColor(MEASURE_COLOR)
        self.line.setPen(pen)

        # self.mark_start = QGraphicsLineItem(*self.start, *self.start)  # will be replaced
        # self.mark_end = QGraphicsLineItem(*self.end, *self.end)

        self.mark_start = pg.ArrowItem(
            angle=180 - self.angle,
            tipAngle=30,
            baseAngle=20,
            headLen=10,
            tailLen=None,
            brush=None,
            pen=pen,
        )
        self.mark_end = pg.ArrowItem(
            angle=-self.angle,
            tipAngle=30,
            baseAngle=20,
            headLen=10,
            tailLen=None,
            brush=None,
            pen=pen,
        )

        self.mark_start.setPos(self.start[0] + self.offset[0], self.start[1] + self.offset[1])
        self.mark_end.setPos(self.end[0] + self.offset[0], self.end[1] + self.offset[1])

        self.offset_start = QGraphicsLineItem(*self.end, *self.end)
        self.offset_end = QGraphicsLineItem(*self.end, *self.end)

        self.offset_start.setPen(pen)
        self.offset_end.setPen(pen)

        target.addItem(self.line, ignoreBounds=not do_bounds)

        target.addItem(self.mark_start, ignoreBounds=not do_bounds)
        target.addItem(self.mark_end, ignoreBounds=not do_bounds)
        target.addItem(self.offset_start, ignoreBounds=not do_bounds)
        target.addItem(self.offset_end, ignoreBounds=not do_bounds)

        self.textitem = pg.TextItem(f"{self.distance:.2f}", anchor=(0.5, 0.5), fill=(254, 254, 254))
        self.textitem.setPos(*self.midpoint)

        if self.angle > 90 or self.angle < -90:
            self.textitem.setAngle(self.angle - 180)
        else:
            self.textitem.setAngle(self.angle)

        self.textitem.setColor(MEASURE_COLOR)

        target.addItem(self.textitem, ignoreBounds=not do_bounds)

        self.offset_start.setLine(
            self.start[0],
            self.start[1],
            self.start[0] + self.offset[0],
            self.start[1] + self.offset[1],
        )

        self.offset_end.setLine(
            self.end[0],
            self.end[1],
            self.end[0] + self.offset[0],
            self.end[1] + self.offset[1],
        )

    @staticmethod
    def _unpack_coordinates(coords):
        """Unpacks a tuple of coordinates (x, y), or returns a fallback if invalid."""
        if isinstance(coords, tuple) and len(coords) == 2:
            return coords
        else:
            # Handle error: coords is not a valid tuple
            return (0, 0)  # Example fallback

    def updateItems(self, target: pg.PlotWidget):
        """Updates the visibility of graphical items based on their presence within the view range of the target PlotWidget.

        Args:
            target (pg.PlotWidget): The PlotWidget whose view range is used to determine the visibility of items.

        Behavior:
            - Checks if the start and end points of the element are within the view range of the target.
            - If both points are within the view, sets all associated graphical items (marks, offsets, line, and text) to visible.
            - If either point is outside the view, hides all associated graphical items.
        """
        if self._invalid:
            return

        view_range = target.viewRect()
        length = max(view_range.width(), view_range.height())
        logger.debug(f"Measure length: {length}")

        # Unpack both self.start and self.end using the helper function
        x1, y1 = self._unpack_coordinates(self.start)
        x2, y2 = self._unpack_coordinates(self.end)

        visible = bool(self.in_view(x1, y1, target) and self.in_view(x2, y2, target))

        self.mark_start.setVisible(visible)
        self.mark_end.setVisible(visible)
        self.offset_start.setVisible(visible)
        self.offset_end.setVisible(visible)
        self.line.setVisible(visible)
        self.textitem.setVisible(visible)

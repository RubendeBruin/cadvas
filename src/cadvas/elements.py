import math
from warnings import warn
from abc import ABC, abstractmethod

from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPolygonF, QBrush
from PySide6.QtWidgets import (
    QGraphicsLineItem,
    QGraphicsRectItem,
    QGraphicsPolygonItem,
    QGraphicsEllipseItem,
)
import PySide6.QtWidgets
import pyqtgraph as pg

MEASURE_COLOR = QColor(0, 200, 150)

"""
Use ,ignoreBounds=True to speed-up adding to plot

"""


class CadItem(ABC):
    @abstractmethod
    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        """Creates items and adds them to target"""
        pass

    @abstractmethod
    def updateItems(self, target: pg.PlotWidget):
        """Updates the items"""
        pass

    def in_view(self, x, y, w):
        range = w.viewRect()
        if x < range.left():
            return False
        if x > range.right():
            return False
        if y > range.bottom():
            return False
        if y < range.top():
            return False
        return True


class Segment(CadItem):
    """Segment is a line between two points"""

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        self.line = QGraphicsLineItem(*self.start, *self.end)
        pen = self.line.pen()
        pen.setWidth(0.1)
        self.line.setPen(pen)
        target.addItem(self.line, ignoreBounds=not do_bounds)

    def updateItems(self, target: pg.PlotWidget):
        pass


class Box(CadItem):
    """Box is a rectangle"""

    def __init__(self, lower_left, upper_right):
        self.lower_left = lower_left
        self.upper_right = upper_right

    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        w = self.upper_right[0] - self.lower_left[0]
        h = self.upper_right[1] - self.lower_left[1]

        self.rect = QGraphicsRectItem(*self.lower_left, w, h)

        pen = self.rect.pen()
        pen.setWidth(0.1)
        self.rect.setPen(pen)
        target.addItem(self.rect, ignoreBounds=not do_bounds)

    def updateItems(self, target: pg.PlotWidget):
        pass


class Polygon(CadItem):
    """Polygon is a closed segment"""

    def __init__(self, points):
        self.points = points

    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        pts = [QPointF(*point) for point in self.points]
        p = QPolygonF(pts)
        self.poly = QGraphicsPolygonItem(p)
        target.addItem(self.poly)

        self.poly.mousePressEvent = self.clicked

    def clicked(self, event):
        self.poly.setBrush(QBrush(QColor(0, 254, 0)))
        self.poly.update()

    def updateItems(self, target: pg.PlotWidget):
        pass


class Circle(CadItem):
    """Polygon is a closed segment"""

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def createItems(self, target: pg.PlotWidget, do_bounds=False):
        self.circle = QGraphicsEllipseItem(
            self.center[0] - self.radius,
            self.center[1] - self.radius,
            2 * self.radius,
            2 * self.radius,
        )
        pen = self.circle.pen()
        pen.setWidth(0.1)
        self.circle.setPen(pen)
        target.addItem(self.circle, ignoreBounds=not do_bounds)

    def updateItems(self, target: pg.PlotWidget):
        pass


class Measure(CadItem):
    def __init__(self, start, end, offset=0):
        """Offset will offset the measurement line to the left side of the endpoint when looking from start to end"""
        self.start = start
        self.end = end

        dx = start[0] - end[0]
        dy = start[1] - end[1]
        self.distance = math.sqrt(dx**2 + dy**2)

        if self.distance == 0:
            warn("Can not create a measurement with length 0")
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
        if self._invalid:
            return

        self.line = QGraphicsLineItem(
            self.start[0] + self.offset[0],
            self.start[1] + self.offset[1],
            self.end[0] + self.offset[0],
            self.end[1] + self.offset[1],
        )
        pen = self.line.pen()
        pen.setWidth(0.1)
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

        self.mark_start.setPos(
            self.start[0] + self.offset[0], self.start[1] + self.offset[1]
        )
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

        self.textitem = pg.TextItem(
            f"{self.distance:.2f}", anchor=(0.5, 0.5), fill=(254, 254, 254)
        )
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

    def updateItems(self, target: pg.PlotWidget):
        if self._invalid:
            return

        range = target.viewRect()
        length = max(range.width(), range.height())

        if self.in_view(*self.start, target) and self.in_view(*self.end, target):
            visible = True

        else:
            visible = False

        self.mark_start.setVisible(visible)
        self.mark_end.setVisible(visible)
        self.offset_start.setVisible(visible)
        self.offset_end.setVisible(visible)
        self.line.setVisible(visible)
        self.textitem.setVisible(visible)

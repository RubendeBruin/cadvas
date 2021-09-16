import math
from abc import ABC,abstractmethod

import  pyqtgraph as pg
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsLineItem, QGraphicsRectItem

MEASURE_COLOR = QColor(0,200,150)

"""
Use ,ignoreBounds=True to speed-up adding to plot

"""

class CadItem(ABC):

    @abstractmethod
    def createItems(self, target : pg.PlotWindow, do_bounds = False):
        """Creates items and adds them to target"""
        pass

    @abstractmethod
    def updateItems(self, target : pg.PlotWindow):
        """Updates the items"""
        pass

    def in_view(self, x,y,w):
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

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def createItems(self, target : pg.PlotWindow, do_bounds = False):
        self.line = QGraphicsLineItem(*self.start, *self.end)
        pen = self.line.pen()
        pen.setWidth(0.1)
        self.line.setPen(pen)
        target.addItem(self.line,ignoreBounds=not do_bounds)

    def updateItems(self, target : pg.PlotWindow):
        pass

class Box(CadItem):

    def __init__(self, lower_left, upper_right):
        self.lower_left = lower_left
        self.upper_right = upper_right

    def createItems(self, target : pg.PlotWindow, do_bounds = False):

        w = self.upper_right[0]- self.lower_left[0]
        h = self.upper_right[1]- self.lower_left[1]

        self.rect = QGraphicsRectItem(*self.lower_left ,w,h)

        pen = self.rect.pen()
        pen.setWidth(0.1)
        self.rect.setPen(pen)
        target.addItem(self.rect, ignoreBounds=not do_bounds)

    def updateItems(self, target : pg.PlotWindow):
        pass

class Measure(CadItem):

    def __init__(self, start, end, offset=0):
        """Offset will offset the measurement line to the left side of the endpoint when looking from start to end"""
        self.start = start
        self.end = end

        dx = start[0]-end[0]
        dy = start[1]-end[1]
        self.distance = math.sqrt(dx**2 + dy**2)

        if self.distance == 0:
            raise ValueError('Can not create a measurement with length 0')

        ndx = dx / self.distance
        ndy = dy / self.distance

        self.offset = (-offset*ndy, offset*ndx)

        self.midpoint = (0.5*(start[0]+end[0]) + self.offset[0], 0.5*(start[1] + end[1]) + self.offset[1])

        self.ndx = ndx
        self.ndy = ndy

        self.angle = math.degrees(math.atan2(dy,dx))

    def createItems(self, target : pg.PlotWindow, do_bounds = False):
        self.line = QGraphicsLineItem(self.start[0] + self.offset[0],
                                      self.start[1] + self.offset[1],
                                      self.end[0] + self.offset[0],
                                      self.end[1] + self.offset[1])
        pen = self.line.pen()
        pen.setWidth(0.1)
        pen.setColor(MEASURE_COLOR)
        self.line.setPen(pen)

        # self.mark_start = QGraphicsLineItem(*self.start, *self.start)  # will be replaced
        # self.mark_end = QGraphicsLineItem(*self.end, *self.end)

        self.mark_start = pg.ArrowItem(angle=180-self.angle, tipAngle=30, baseAngle=20, headLen=10, tailLen=None, brush=None, pen=pen)
        self.mark_end = pg.ArrowItem(angle=-self.angle, tipAngle=30, baseAngle=20, headLen=10, tailLen=None, brush=None, pen=pen)

        self.mark_start.setPos(self.start[0] + self.offset[0],
                                      self.start[1] + self.offset[1])
        self.mark_end.setPos(self.end[0] + self.offset[0],
                                      self.end[1] + self.offset[1])

        self.offset_start = QGraphicsLineItem(*self.end, *self.end)
        self.offset_end = QGraphicsLineItem(*self.end, *self.end)

        self.offset_start.setPen(pen)
        self.offset_end.setPen(pen)

        target.addItem(self.line,ignoreBounds=not do_bounds)

        target.addItem(self.mark_start,ignoreBounds=not do_bounds)
        target.addItem(self.mark_end,ignoreBounds=not do_bounds)
        target.addItem(self.offset_start,ignoreBounds=not do_bounds)
        target.addItem(self.offset_end,ignoreBounds=not do_bounds)

        self.textitem = pg.TextItem(f'{self.distance:.2f}', anchor=(0.5, 0.5), fill=(254,254,254))
        self.textitem.setPos(*self.midpoint)

        if self.angle > 90 or self.angle < -90:
            self.textitem.setAngle(self.angle - 180)
        else:
            self.textitem.setAngle(self.angle)

        self.textitem.setColor(MEASURE_COLOR)

        target.addItem(self.textitem,ignoreBounds=not do_bounds)

        self.offset_start.setLine(self.start[0],
                                  self.start[1],
                                  self.start[0] + self.offset[0],
                                  self.start[1] + self.offset[1],
                                  )

        self.offset_end.setLine(self.end[0],
                                self.end[1],
                                self.end[0] + self.offset[0],
                                self.end[1] + self.offset[1],
                                )

    def updateItems(self, target : pg.PlotWindow):

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


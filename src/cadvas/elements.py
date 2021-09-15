import math
from abc import ABC,abstractmethod

import  pyqtgraph as pg
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsLineItem, QGraphicsRectItem

MEASURE_COLOR = QColor(0,200,150)

"""
Use ,ignoreBounds=True to speed-up adding to plot

"""

class Item(ABC):

    @abstractmethod
    def createItems(self, target : pg.PlotWindow):
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



class Segment(Item):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def createItems(self, target : pg.PlotWindow):
        self.line = QGraphicsLineItem(*self.start, *self.end)
        pen = self.line.pen()
        pen.setWidth(0.1)
        self.line.setPen(pen)
        target.addItem(self.line,ignoreBounds=True)

    def updateItems(self, target : pg.PlotWindow):
        pass

class Box(Item):

    def __init__(self, lower_left, upper_right):
        self.lower_left = lower_left
        self.upper_right = upper_right

    def createItems(self, target : pg.PlotWindow):

        w = self.upper_right[0]- self.lower_left[0]
        h = self.upper_right[1]- self.lower_left[1]

        self.rect = QGraphicsRectItem(*self.lower_left ,w,h)

        pen = self.rect.pen()
        pen.setWidth(0.1)
        self.rect.setPen(pen)
        target.addItem(self.rect, ignoreBounds=True)

    def updateItems(self, target : pg.PlotWindow):
        pass

class Measure(Item):

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.distance = math.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
        self.midpoint = (0.5*(start[0]+end[0]), 0.5*(start[1] + end[1]))

    def createItems(self, target : pg.PlotWindow):
        self.line = QGraphicsLineItem(*self.start, *self.end)
        pen = self.line.pen()
        pen.setWidth(0.1)
        pen.setColor(MEASURE_COLOR)
        self.line.setPen(pen)

        self.mark_start = QGraphicsLineItem(*self.start, *self.start)
        self.mark_end = QGraphicsLineItem(*self.end, *self.end)

        self.mark_start.setPen(pen)
        self.mark_end.setPen(pen)

        target.addItem(self.line,ignoreBounds=True)

        target.addItem(self.mark_start,ignoreBounds=True)
        target.addItem(self.mark_end,ignoreBounds=True)

        self.textitem = pg.TextItem(f'{self.distance:.2f}')
        self.textitem.setPos(*self.midpoint)
        self.textitem.setColor(MEASURE_COLOR)

        target.addItem(self.textitem,ignoreBounds=True)



    def updateItems(self, target : pg.PlotWindow):

        range = target.viewRect()
        length = max(range.width(), range.height())

        if self.in_view(*self.start, target) and self.in_view(*self.end, target):

            w = 0.01 * length
            self.mark_start.setLine(self.start[0]-0.7*w, self.start[1]-w, self.start[0]+0.7*w, self.start[1]+w)
            self.mark_end.setLine(self.end[0]-0.7*w, self.end[1]-w, self.end[0]+0.7*w, self.end[1]+w)

            visible = True

        else:
            visible = False


        self.mark_start.setVisible(visible)
        self.mark_end.setVisible(visible)
        self.line.setVisible(visible)
        self.textitem.setVisible(visible)

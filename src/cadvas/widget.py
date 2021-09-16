import math

import PySide2
import  pyqtgraph as pg
from PySide2 import QtGui
from PySide2.QtGui import QPen
from PySide2.QtWidgets import QApplication, QGraphicsSimpleTextItem, QGraphicsLineItem
from PySide2.QtWidgets import QWidget, QVBoxLayout

from cadvas.elements import *

# Create a plot

class QCadvasWidget(pg.GraphicsLayoutWidget):

    def __init__(self, *args, **kwargs):
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
        for p in self._items:
            p.updateItems(self.w)

    def addCadItem(self, item: CadItem, do_bounds = False):
        item.createItems(self.w, do_bounds)
        self._items.append(item)


if __name__ == '__main__':

    app = pg.mkQApp()
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('pyqtgraph example: PlotWidget')
    mw.resize(800,800)
    cw = QCadvasWidget()
    mw.setCentralWidget(cw)

    items = []

    seg = Segment((0,1),(10,1))
    cw.addCadItem(seg, do_bounds=True)

    seg = Segment((0,5),(10,1))
    cw.addCadItem(seg, do_bounds=True)

    meas = Measure((4,1),(0,5), offset=0.5)
    cw.addCadItem(meas)

    meas = Measure((4,1),(2,1), offset=0.5)
    cw.addCadItem(meas)

    meas = Measure((2,1),(2,10), offset=0.5)
    cw.addCadItem(meas)

    box = Box((-10,-10),(10,10))
    cw.addCadItem(box, do_bounds=True)

    for i in range(36):
        cw.addCadItem(Measure((0,0),
                              (10 * math.cos(math.radians(10*i)), 10 * math.sin(math.radians(10*i)))))


    mw.show()

    app = QApplication.instance()
    app.exec_()



#
# import pyqtgraph.exporters
#
# exporter = pyqtgraph.exporters.ImageExporter( w.scene() )
# exporter.parameters()['width'] = 8000
# exporter.export(r'c:\data\test.png')
#
# print('done')
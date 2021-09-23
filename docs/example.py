import PySide2
import pyqtgraph as pg
from PySide2 import QtGui
from PySide2.QtWidgets import QApplication
from cadvas import *


app = pg.mkQApp()
mw = QtGui.QMainWindow()
mw.setWindowTitle('pyqtgraph example: PlotWidget')
mw.resize(800, 800)
cw = QCadvasWidget()
mw.setCentralWidget(cw)

items = []

seg = Segment((0, 1), (10, 1))
cw.addCadItem(seg, do_bounds=True)

seg = Segment((0, 5), (10, 1))
cw.addCadItem(seg, do_bounds=True)

meas = Measure((4, 1), (0, 5), offset=0.5)
cw.addCadItem(meas)

meas = Measure((4, 1), (2, 1), offset=0.5)
cw.addCadItem(meas)

meas = Measure((2, 1), (2, 10), offset=0.5)
cw.addCadItem(meas)

box = Box((-10, -10), (10, 10))
cw.addCadItem(box, do_bounds=True)


mw.show()

app = QApplication.instance()
app.exec_()
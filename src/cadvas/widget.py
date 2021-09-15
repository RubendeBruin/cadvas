import PySide2
import  pyqtgraph as pg
from PySide2.QtGui import QPen
from PySide2.QtWidgets import QApplication, QGraphicsSimpleTextItem, QGraphicsLineItem

from cadvas.elements import *

# Create a plot

app = pg.mkQApp()

w = pg.PlotWidget()
w.setAspectLocked(True)
w.setBackground((254,254,254))
w.enableAutoRange(False)


items = []

seg = Segment((0,1),(10,1))
seg.createItems(w)
items.append(seg)

seg = Segment((0,5),(10,1))
seg.createItems(w)
items.append(seg)

meas = Measure((0,5),(0,1))
meas.createItems(w)
items.append(meas)

box = Box((1,1),(3,10))
box.createItems(w)
items.append(box)

print('adding')

for i in range(100):
    meas = Measure((i, i+5), (i+3, 3*i))
    meas.createItems(w)
    items.append(meas)

print('done')

def changed():
    for p in items:
        p.updateItems(w)

w.sigRangeChanged.connect(changed)

w.show()

app = QApplication.instance()
app.exec_()

print('done')
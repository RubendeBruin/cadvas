import pyqtgraph as pg

from .elements import CadItem

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

    def addCadItem(self, item: CadItem, do_bounds=True):
        item.createItems(self.w, do_bounds)
        self._items.append(item)

    def clearDrawing(self):
        self._items = []
        self.w.clear()
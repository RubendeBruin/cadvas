
import math
import pyqtgraph as pg
from cadvas import QCadvasWidget, Box, Circle, Measure, Polygon, Segment
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication


def show_cad_drawing():
    app = pg.mkQApp()
    mw = QtWidgets.QMainWindow()
    mw.setWindowTitle("pyqtgraph example: PlotWidget")
    mw.resize(800, 800)
    cw = QCadvasWidget()
    mw.setCentralWidget(cw)

    items = []

    seg = Segment((0, 1), (10, 1))
    cw.addCadItem(seg, do_bounds=True)

    seg = Segment((0, 5), (11, 1))
    cw.addCadItem(seg, do_bounds=True)

    meas = Measure((4, 1), (0, 5), offset=0.5)
    cw.addCadItem(meas)

    meas = Measure((4, 1), (2, 1), offset=0.5)
    cw.addCadItem(meas)

    meas = Measure((2, 1), (2, 10), offset=0.5)
    cw.addCadItem(meas)

    box = Box((-10, -10), (10, 10))
    cw.addCadItem(box, do_bounds=True)

    for i in range(36):
        cw.addCadItem(Measure((0, 0), (10 * math.cos(math.radians(10 * i)), 10 * math.sin(math.radians(10 * i)))))

    poly = Polygon(((0, 0), (0, 1), (1, 0)))
    cw.addCadItem(poly)

    rondje = Circle(center=(2, 2), radius=2)
    cw.addCadItem(rondje)

    mw.show()

    # cw.clearDrawing()

    box = Box((-10, -10), (10, 10))
    cw.addCadItem(box, do_bounds=True)

    app = QApplication.instance()
    app.exec()

def main():
    show_cad_drawing()


if __name__ == "__main__":
    main()
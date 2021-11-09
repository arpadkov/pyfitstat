from PyQt5 import QtWidgets, QtCore

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import sys







class PlotWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.setMinimumSize(500, 500)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def plot_bar(self, ):




def main():
    test_app = QtWidgets.QApplication(sys.argv)
    window = PlotWidget()
    window.show()
    sys.exit(test_app.exec_())



if __name__ == "__main__":
    main()
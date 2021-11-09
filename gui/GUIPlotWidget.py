from PyQt5 import QtWidgets, QtCore

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PlotWidget(QtWidgets.QWidget):

    plot_clicked = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.parent = parent
        # self.activities = parent.activities

        self.setMinimumSize(500, 500)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.figure.canvas.mpl_connect('pick_event', self.artist_clicked)
        self.figure.canvas.mpl_connect('motion_notify_event', self.mouse_motion)
        # self.figure.canvas.mpl_connect('figure_enter_event', self.parent.show_popup)
        self.figure.canvas.mpl_connect('figure_leave_event', self.parent.mouse_left)

        # self.setMouseTracking(True)
        # self.positionChanged.connect(self.cursor_changed)

        self.bars = []
        self.ax = None
        self.annotations = []
        self.states = []

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def artist_clicked(self, event):

        self.plot_clicked.emit(event.artist.get_gid())

    def plot(self):

        plot_data = self.parent.model.plot_data

        self.figure.clear()
        self.bars = []
        self.ax = None

        self.ax = self.figure.add_subplot(111)

        for i in range(len(plot_data.values)):
            self.bars.append(self.ax.bar(plot_data.labels[i], plot_data.values[i], gid=i, picker=1, color='royalblue'))

        plt.title(plot_data.title)

        self.canvas.draw()

    def mouse_motion(self, event):

        if event.inaxes == self.ax:

            for bar, annot in zip(self.bars, self.annotations):
                cont, ind = bar.patches[0].contains(event)

                if cont:
                    annot.set_state(True)

                else:
                    annot.set_state(False)
from PyQt5 import QtWidgets, QtCore
from pyfitstat.gui.GUIInfoboxWidget import InfoWidget

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PlotWidget(QtWidgets.QWidget):
    positionChanged = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.parent = parent
        # self.activities = parent.activities

        self.setMinimumSize(500, 500)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.figure.canvas.mpl_connect('pick_event', self.parent.artist_clicked)
        self.figure.canvas.mpl_connect('motion_notify_event', self.mouse_motion)
        # self.figure.canvas.mpl_connect('figure_enter_event', self.parent.show_popup)
        self.figure.canvas.mpl_connect('figure_leave_event', self.parent.mouse_left)

        self.setMouseTracking(True)
        self.positionChanged.connect(self.cursor_changed)

        self.bars = []
        self.ax = None
        self.annotations = []
        self.states = []
        # self.plot_data = None

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def mouse_motion(self, event):

        if event.inaxes == self.ax:

            for bar, annot in zip(self.bars, self.annotations):
                cont, ind = bar.patches[0].contains(event)


                if cont:
                    annot.set_state(True)

                else:
                    annot.set_state(False)


    def plot(self, plot_data):

        plot_data = self.edit_plot_data(plot_data)

        self.figure.clear()
        self.bars = []
        self.ax = None
        self.annotations = []

        self.ax = self.figure.add_subplot(111)

        # self.annotation = self.ax.annotate('AA', xy=(1, 1), ha='center')

        for i in range(len(plot_data["values"])):
            self.bars.append(self.ax.bar(plot_data["labels"][i], plot_data["values"][i], gid=i, picker=1, color='royalblue'))

            annot = InfoWidget(label=str(round(plot_data["values"][i], 2)))
            self.annotations.append(annot)
            self.states.append(False)

            # self.annotations.append(self.get_annotation(key=i))

        # for annot in self.annotations:
            # annot.widget.setGeometry = self.frameGeometry()

        plt.title(plot_data["title"])

        self.canvas.draw()

    def edit_plot_data(self, plot_data):

        if plot_data["act_info"] == 'distance':
            values = plot_data["values"]
            plot_data["values"] = [value/1000 for value in values]

        return plot_data

    def get_annotation(self, key):

        if self.parent.current_info == 'distance':
            return DistanceAnnotation(self.ax, data=self.plot_data, key=key).return_annot_widget()
        else:
            return None

    @QtCore.pyqtSlot(QtCore.QPoint)
    def cursor_changed(self, pos):
        print(pos)


class DistanceAnnotation:

    def __init__(self, axes, data, key):

        self._axes = axes
        self._data = data
        self._key = key

        self.widget = None

    def return_annot(self):
        bbox = dict(boxstyle="round", fc="0.8")

        distance = round(self._data["values"][self._key])
        year = self._data["labels"][self._key]

        data = str(distance) + ' km' + '\n' + str(year)


        # return [distance, year]
        return self._axes.annotate(
                data,
                xy=(self._key, max(self._data["values"]) / 2),
                ha='center',
                bbox=bbox,
                visible=False
            )

    def return_annot_widget(self):

        self.widget = InfoWidget()

        distance = str(round(self._data["values"][self._key])) + ' km'
        year = str(self._data["labels"][self._key])

        self.widget.layout.addWidget(QtWidgets.QLabel(distance))
        self.widget.layout.addWidget(QtWidgets.QLabel(year))

        return self

    def set_visible(self, visible):
        if visible:
            self.widget.show()
        else:
            self.widget.hide()

    def hide_widget(self):
        self.widget.hide()

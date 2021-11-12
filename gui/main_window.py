from pyfitstat.gui.GUIPlotWidget import PlotWidget
from pyfitstat.gui.GUICalendarSelection import CalendarSelector
from pyfitstat.gui.GUIInfoSelection import InfoSelector

from pyfitstat.model.project_model import ViewType

from PyQt5 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):

    plot_position_changed = QtCore.pyqtSignal()

    def __init__(self, model, parent=None):
        super(MainWindow, self).__init__(parent)

        self.model = model

        layout = QtWidgets.QVBoxLayout()

        self.plot_widget = PlotWidget(parent=self)
        self.plot_widget.plot_clicked.connect(self.model.plot_clicked)

        self.calendar_selection = CalendarSelector(parent=self)
        self.calendar_selection.calendar_change.connect(self.model.calendar_change)

        self.info_selection = InfoSelector(parent=self)

        self.model.message_obj.selection_changed.connect(self.plot_widget.plot)
        self.plot_position_changed.connect(self.plot_widget.move_annotations)

        layout.addWidget(self.calendar_selection)
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.info_selection)

        window = QtWidgets.QWidget()
        window.setLayout(layout)
        self.setCentralWidget(window)

        # self.plot_widget.plot()

    # def plot_widget_pos(self):
    #     return self.plot_widget.mapToGlobal(QtCore.QPoint(0, 0))

    def resizeEvent(self, event):
        self.plot_position_changed.emit()

    def moveEvent(self, event):
        self.plot_position_changed.emit()

    def keyPressEvent(self, event) -> None:
        print(event.key())



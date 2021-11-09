from pyfitstat.gui.GUIPlotWidget import PlotWidget
from pyfitstat.gui.GUICalendarSelection import CalendarSelector
from pyfitstat.gui.GUIInfoSelection import InfoSelector

from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):

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

        layout.addWidget(self.calendar_selection)
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.info_selection)

        window = QtWidgets.QWidget()
        window.setLayout(layout)
        self.setCentralWidget(window)

        self.plot_widget.plot()

    def keyPressEvent(self, event) -> None:
        print(event.key())

    def mouse_left(self, event):

        for annot in self.plot_widget.annotations:
            annot.hide()
            self.plot_widget.canvas.draw()

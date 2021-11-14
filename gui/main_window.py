from pyfitstat.gui.GUIPlotWidget import PlotWidget
from pyfitstat.gui.GUICalendarSelection import CalendarSelector
from pyfitstat.gui.GUIInfoSelection import InfoSelector
from pyfitstat.gui.GUILogging import GUILogging
from pyfitstat.gui.GUIConsole import ConsoleWidget

from pyfitstat.model.project_model import ViewType

from PyQt5 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):

    plot_position_changed = QtCore.pyqtSignal()

    def __init__(self, model, parent=None):
        super(MainWindow, self).__init__(parent)

        self.model = model

        self.layout = QtWidgets.QVBoxLayout()

        self.createMenus()
        self.createDockWindows()

        self.create_main_view()

        window = QtWidgets.QWidget()
        window.setLayout(self.layout)
        self.setCentralWidget(window)

        self.show()

        self.move(300, 100)

        # self.sizeHint()

        # self.model.sync_activities()

        # self.plot_widget.plot()

    # def plot_widget_pos(self):
    #     return self.plot_widget.mapToGlobal(QtCore.QPoint(0, 0))

    def create_main_view(self):

        self.plot_widget = PlotWidget(parent=self)
        self.plot_widget.plot_clicked.connect(self.model.plot_clicked)

        self.calendar_selection = CalendarSelector(parent=self)
        self.calendar_selection.calendar_change.connect(self.model.calendar_change)

        self.model.message_obj.selection_changed.connect(self.plot_widget.plot)
        self.plot_position_changed.connect(self.plot_widget.move_annotations)

        self.info_selection = InfoSelector(parent=self)

        self.layout.addWidget(self.calendar_selection)
        self.layout.addWidget(self.plot_widget)
        self.layout.addWidget(self.info_selection)

    # def update_model(self, model):
    #     self.model = model
    #     self.plot_widget.model = self.model

    def createDockWindows(self):

        dock_logging = QtWidgets.QDockWidget("Logging", self)
        dock_logging.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.logging_widget = GUILogging()
        dock_logging.setWidget(self.logging_widget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock_logging)
        self.viewMenu.addAction(dock_logging.toggleViewAction())

        dock_console = QtWidgets.QDockWidget("Console", self)
        dock_console.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.console_widget = ConsoleWidget()
        self.console_widget.push_vars({"data": self.model})
        dock_console.setWidget(self.console_widget)

        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock_console)
        self.tabifyDockWidget(dock_logging, dock_console)
        dock_logging.raise_()

        self.setTabPosition(QtCore.Qt.BottomDockWidgetArea, QtWidgets.QTabWidget.North)

        self.viewMenu.addAction(dock_console.toggleViewAction())

    def createMenus(self):

        self.fileMenu = self.menuBar().addMenu("&File")

        self.viewMenu = self.menuBar().addMenu("&View")

    def resizeEvent(self, event):
        self.plot_position_changed.emit()

    def moveEvent(self, event):
        self.plot_position_changed.emit()

    def keyPressEvent(self, event) -> None:
        print(event.key())



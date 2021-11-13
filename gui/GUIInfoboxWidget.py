from PyQt5 import QtWidgets, QtCore, QtGui


class InfoWidget(QtWidgets.QWidget):

    def __init__(self, label, state=False, parent=None):
        super(InfoWidget, self).__init__(parent)

        self.state = state

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.ToolTip)

        self.layout = QtWidgets.QVBoxLayout()

        # self.setGeometry(100, 100, 100, 100)
        self.setFixedSize(100, 70)

        # self.label = QtWidgets.QLabel(label)
        # self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        self.move_to()

    def move_to(self):
        pass

    def set_state(self, state):

        if state != self.state:
            self.state = state
            self.state_changed(state)

    def state_changed(self, state):
        if state:
            self.show()

        else:
            self.hide()


class DistanceInfobox(InfoWidget):

    def __init__(self, value, parent=None):
        super(DistanceInfobox, self).__init__(parent)

        self.title = QtWidgets.QLabel('Distance')
        self.title.setFont(QtGui.QFont('Arial', 12))

        self.value_label = QtWidgets.QLabel(str(round(value/1000, 2)) + ' km')

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.value_label)


class ElevationInfobox(InfoWidget):

    def __init__(self, parent=None):
        super(ElevationInfobox, self).__init__(parent)


class DurationInfobox(InfoWidget):

    def __init__(self, parent=None):
        super(DurationInfobox, self).__init__(parent)


class ActivityInfobox(InfoWidget):

    def __init__(self, parent=None):
        super(ActivityInfobox, self).__init__(parent)

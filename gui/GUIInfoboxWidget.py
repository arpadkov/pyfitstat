from PyQt5 import QtWidgets, QtCore


class InfoWidget(QtWidgets.QWidget):

    def __init__(self, label, state=False):
        super(InfoWidget, self).__init__()

        self.state = state

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.ToolTip)

        self.layout = QtWidgets.QVBoxLayout()

        # self.setGeometry(100, 100, 100, 100)
        self.setFixedSize(100, 100)

        self.label = QtWidgets.QLabel(label)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

    def set_state(self, state):

        if state != self.state:
            self.state = state
            self.state_changed(state)

    def state_changed(self, state):
        if state:
            self.show()
            print('Showing')

        else:
            self.hide()
            print('Hiding')


class TestWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(TestWidget, self).__init__(parent)


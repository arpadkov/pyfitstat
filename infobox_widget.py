from PyQt5 import QtWidgets, QtCore


class InfoWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.ToolTip)

        self.layout = QtWidgets.QVBoxLayout()

        # self.setGeometry(100, 100, 100, 100)
        self.setFixedSize(100, 100)
        # self.layout.addWidget(QtWidgets.QLabel('aaa'))

        self.setLayout(self.layout)


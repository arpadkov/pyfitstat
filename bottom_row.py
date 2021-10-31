from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal


class BottomRow(QtWidgets.QWidget):

    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.layout = QtWidgets.QHBoxLayout()

        self.distance_button = QtWidgets.QPushButton('Distance')
        self.distance_button.clicked.connect(self.parent.show_distance)

        self.duration_button = QtWidgets.QPushButton('Duration')
        self.duration_button.clicked.connect(self.parent.show_duration)

        self.elevationgain_button = QtWidgets.QPushButton('Elevation Gain')
        self.elevationgain_button.clicked.connect(self.parent.show_elevation_gain)

        self.elevationloss_button = QtWidgets.QPushButton('Elevation Loss')
        self.elevationloss_button.clicked.connect(self.parent.show_elevation_loss)

        self.layout.addWidget(self.distance_button)
        self.layout.addWidget(self.duration_button)
        self.layout.addWidget(self.elevationgain_button)
        self.layout.addWidget(self.elevationloss_button)

        self.setLayout(self.layout)


from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal


class BottomRow(QtWidgets.QWidget):

    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.layout = QtWidgets.QHBoxLayout()

        self.distance_button = QtWidgets.QPushButton('Distance')
        self.distance_button.clicked.connect(self.distance_clicked)
        self.distance_button.setCheckable(True)
        self.distance_button.setChecked(True)

        self.duration_button = QtWidgets.QPushButton('Duration')
        self.duration_button.clicked.connect(self.duration_clicked)
        self.duration_button.setCheckable(True)

        self.elevationgain_button = QtWidgets.QPushButton('Elevation Gain')
        self.elevationgain_button.clicked.connect(self.elevation_gain_clicked)
        self.elevationgain_button.setCheckable(True)

        self.elevationloss_button = QtWidgets.QPushButton('Elevation Loss')
        self.elevationloss_button.clicked.connect(self.elevation_loss_clicked)
        self.elevationloss_button.setCheckable(True)

        self.buttons = [
            self.distance_button,
            self.duration_button,
            self.elevationgain_button,
            self.elevationloss_button,
        ]

        self.layout.addWidget(self.distance_button)
        self.layout.addWidget(self.duration_button)
        self.layout.addWidget(self.elevationgain_button)
        self.layout.addWidget(self.elevationloss_button)

        self.setLayout(self.layout)

    def distance_clicked(self):

        for button in self.buttons:
            button.setChecked(False)

        self.distance_button.setChecked(True)

        self.parent.show_distance()

    def duration_clicked(self):

        for button in self.buttons:
            button.setChecked(False)

        self.duration_button.setChecked(True)

        self.parent.show_duration()

    def elevation_gain_clicked(self):

        for button in self.buttons:
            button.setChecked(False)

        self.elevationgain_button.setChecked(True)

        self.parent.show_elevation_gain()

    def elevation_loss_clicked(self):

        for button in self.buttons:
            button.setChecked(False)

        self.elevationloss_button.setChecked(True)

        self.parent.show_elevation_loss()
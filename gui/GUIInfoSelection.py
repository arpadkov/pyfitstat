from pyfitstat.model.project_model import ActivityInfo

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal


class InfoSelector(QtWidgets.QWidget):

    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.layout = QtWidgets.QHBoxLayout()

        self.distance_button = InfoButton(self.parent.model, ActivityInfo.Distance, parent=self)
        self.duration_button = InfoButton(self.parent.model, ActivityInfo.Duration, parent=self)
        self.elevationgain_button = InfoButton(self.parent.model, ActivityInfo.ElevationGain, parent=self)
        self.elevationloss_button = InfoButton(self.parent.model, ActivityInfo.ElevationLoss, parent=self)

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


class InfoButton(QtWidgets.QPushButton):

    def __init__(self, model, info: ActivityInfo, parent=None):
        super(InfoButton, self).__init__()

        self.model = model
        self.info = info
        self.parent = parent

        self.setText(self.info.name)
        self.setCheckable(True)

        if self.model.act_info == self.info:
            self.setChecked(True)

        self.clicked.connect(self.button_clicked)

    def button_clicked(self):

        self.model.act_info = self.info

        for button in self.parent.buttons:
            button.setChecked(False)

        self.setChecked(True)



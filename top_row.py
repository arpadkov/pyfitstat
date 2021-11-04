import os

from PyQt5 import QtWidgets, QtCore, QtGui

from pyfitstat.model.model import ViewType


class TopRow(QtWidgets.QWidget):

    act_type_change = QtCore.pyqtSignal(object)
    view_type_change = QtCore.pyqtSignal(object)
    calender_change = QtCore.pyqtSignal(object)
    # calender_right = pyqtSignal()
    # calender_left = pyqtSignal()

    data_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.cb_calender = QtWidgets.QComboBox()
        self.cb_calender.names = [option.name.capitalize() for option in ViewType]
        self.cb_calender.options = [option for option in ViewType]
        for name in self.cb_calender.names:
            self.cb_calender.addItem(name)
        self.cb_calender.currentIndexChanged.connect(self.view_type_changed)
        self.cb_calender.setFixedSize(100, 30)

        self.cb_activity_type = QtWidgets.QComboBox()
        self.cb_activity_type.addItem('Running')
        self.cb_activity_type.addItem('Cycling')
        self.cb_activity_type.addItem('Hiking')
        self.cb_activity_type.currentTextChanged.connect(self.act_type_changed)
        self.cb_activity_type.setFixedSize(100, 30)

        self.right_button = ArrowButton('right')
        self.right_button.clicked.connect(self.right_click)

        self.left_button = ArrowButton('left')
        self.left_button.clicked.connect(self.left_click)

        self.layout = QtWidgets.QHBoxLayout()

        self.layout.addWidget(self.left_button)
        self.layout.addWidget(self.cb_calender)
        self.layout.addWidget(self.cb_activity_type)
        self.layout.addWidget(self.right_button)

        self.setLayout(self.layout)

    def right_click(self):
        self.calender_change.emit(1)
        self.data_changed.emit()

    def left_click(self):
        self.calender_change.emit(-1)
        self.data_changed.emit()

    def act_type_changed(self):
        self.act_type_change.emit(self.cb_activity_type.currentText())
        self.data_changed.emit()

    def view_type_changed(self, index):
        self.view_type_change.emit(self.cb_calender.options[index])
        self.data_changed.emit()

    # def reset_combos(self):
    #
    #     self.cb_calender.setCurrentText(self.parent.current_view)
    #     self.cb_activity_type.setCurrentText(self.parent.current_type)


class ArrowButton(QtWidgets.QPushButton):

    def __init__(self, direction: str):
        super().__init__()

        self.size = QtCore.QSize(60, 60)
        self.icon = QtGui.QIcon(os.path.join(os.getcwd(), 'icons', f'arrow_{direction}.png'))
        self.setFixedSize(self.size)
        self.setIconSize(self.size * 0.9)
        self.setIcon(self.icon)
        self.setFlat(True)
        # self.setStyleSheet('border: none')

        # print(self.isFlat())






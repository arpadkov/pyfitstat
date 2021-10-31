from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal


class TopRow(QtWidgets.QWidget):

    act_type_change = pyqtSignal(object)
    view_type_change = pyqtSignal(object)
    calender_right = pyqtSignal()
    calender_left = pyqtSignal()

    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.cb_calender = QtWidgets.QComboBox()
        self.cb_calender.addItem('All')
        self.cb_calender.addItem('Year')
        self.cb_calender.addItem('Month')
        self.cb_calender.currentTextChanged.connect(self.view_type_changed)
        self.cb_calender.setFixedSize(100, 30)

        self.cb_activity_type = QtWidgets.QComboBox()
        self.cb_activity_type.addItem('Running')
        self.cb_activity_type.addItem('Cycling')
        self.cb_activity_type.addItem('Hiking')
        self.cb_activity_type.currentTextChanged.connect(self.act_type_changed)
        self.cb_activity_type.setFixedSize(100, 30)

        self.right_button = QtWidgets.QPushButton()
        self.right_button.clicked.connect(self.right_click)
        self.right_button.setFixedSize(30, 30)

        self.left_button = QtWidgets.QPushButton()
        self.left_button.clicked.connect(self.left_click)
        self.left_button.setFixedSize(30, 30)

        self.layout = QtWidgets.QHBoxLayout()

        self.layout.addWidget(self.left_button)
        self.layout.addWidget(self.cb_calender)
        self.layout.addWidget(self.cb_activity_type)
        self.layout.addWidget(self.right_button)

        self.setLayout(self.layout)

    def right_click(self):
        self.calender_rigth.emit()
        self.data_changed.emit()

    def left_click(self):
        self.calender_left.emit()
        self.data_changed.emit()

    def act_type_changed(self):
        self.act_type_change.emit(self.cb_activity_type.currentText())
        self.data_changed.emit()

    def view_type_changed(self):
        self.view_type_change.emit(self.cb_calender.currentText())
        self.data_changed.emit()

    # def reset_combos(self):
    #
    #     self.cb_calender.setCurrentText(self.parent.current_view)
    #     self.cb_activity_type.setCurrentText(self.parent.current_type)





from PyQt5 import QtWidgets, QtCore, QtGui

import os


class CalendarSelector(QtWidgets.QWidget):

    calendar_change = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.view_type_selector = TypeSelector(self.parent.model, 'view_type', parent=self)
        self.act_type_selector = TypeSelector(self.parent.model, 'act_type', parent=self)

        self.right_button = ArrowButton('right', parent=self)
        self.left_button = ArrowButton('left', parent=self)

        self.layout = QtWidgets.QHBoxLayout()

        self.layout.addWidget(self.left_button)
        self.layout.addWidget(self.view_type_selector)
        self.layout.addWidget(self.act_type_selector)
        self.layout.addWidget(self.right_button)

        self.setLayout(self.layout)


class TypeSelector(QtWidgets.QComboBox):

    def __init__(self, model, attr: str, parent=None):
        super().__init__()

        self.model = model
        self.attr = attr
        self.parent = parent

        self.names = [option.name.capitalize() for option in getattr(self.model, self.attr).__class__]
        self.options = [option for option in getattr(self.model, self.attr).__class__]

        for name in self.names:
            self.addItem(name)

        self.setFixedSize(100, 30)

        self.currentIndexChanged.connect(self.index_changed)
        self.model.message_obj.selection_changed.connect(self.value_changed)

    def index_changed(self, index):
        value = self.options[index]
        setattr(self.model, self.attr, value)

    def value_changed(self):
        index = self.options.index(getattr(self.model, self.attr))
        self.setCurrentIndex(index)


class ArrowButton(QtWidgets.QPushButton):

    def __init__(self, direction: str, parent=None):
        super().__init__()

        self.direction = direction
        self.parent = parent

        self.size = QtCore.QSize(60, 60)
        self.setFixedSize(self.size)

        self.icon = QtGui.QIcon(os.path.join(os.getcwd(), 'icons', f'arrow_{self.direction}.png'))
        self.setIconSize(self.size * 0.9)
        self.setIcon(self.icon)

        self.setFlat(True)

        self.clicked.connect(self.button_clicked)

    def button_clicked(self):

        if self.direction == 'right':
            self.parent.calendar_change.emit(1)

        elif self.direction == 'left':
            self.parent.calendar_change.emit(-1)









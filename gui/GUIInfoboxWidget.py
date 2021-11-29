from pyfitstat.model.project_model import ViewType, ActivityInfo

from PyQt5 import QtWidgets, QtCore, QtGui


class InfoWidget(QtWidgets.QWidget):

    def __init__(self, label, state=False, parent=None):
        super(InfoWidget, self).__init__(parent)

        self.state = state

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.ToolTip)

        self.setStyleSheet("QLabel{font-size: 10pt;}")

        self.title_font = QtGui.QFont()
        self.title_font.setBold(True)
        self.title = QtWidgets.QLabel()
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(self.title_font)
        self.title.setStyleSheet("QLabel{font-size: 12pt; }")
        self.title.setWordWrap(True)


        self.layout = QtWidgets.QGridLayout()



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


# class DistanceInfobox(InfoWidget):
#
#     def __init__(self, value, parent=None):
#         super(DistanceInfobox, self).__init__(parent)
#
#         self.title = QtWidgets.QLabel('Distance')
#         self.title.setFont(QtGui.QFont('Arial', 12))
#
#         self.value_label = QtWidgets.QLabel(str(round(value/1000, 2)) + ' km')
#
#         self.layout.addWidget(self.title)
#         self.layout.addWidget(self.value_label)


# class ElevationInfobox(InfoWidget):
#
#     def __init__(self, parent=None):
#         super(ElevationInfobox, self).__init__(parent)
#
#
# class DurationInfobox(InfoWidget):
#
#     def __init__(self, parent=None):
#         super(DurationInfobox, self).__init__(parent)


class ListSummaryInfobox(InfoWidget):

    def __init__(self, summary, parent=None):
        super(ListSummaryInfobox, self).__init__(parent)

        self.summary = summary


        # title_font.setPointSize(15)

        # self.title = QtWidgets.QLabel(self.summary.title)
        self.title.setText(self.summary.title)


        self.distance = QtWidgets.QLabel('Distance:')
        self.distance_value = QtWidgets.QLabel(str(round(self.summary.distance / 1000, 2)))
        self.distance_unit = QtWidgets.QLabel('km')

        self.elevation_gain = QtWidgets.QLabel('Elevation gain:')
        self.elevation_gain_value = QtWidgets.QLabel(str(round(self.summary.elevation_gain / 1000, 2)))
        self.elevation_gain_unit = QtWidgets.QLabel('km')

        self.duration = QtWidgets.QLabel('Duration:')
        self.duration_value = QtWidgets.QLabel(format_seconds_to_hhmmss(self.summary.duration))
        self.duration_unit = QtWidgets.QLabel('')

        # self.distance = QtWidgets.QLabel('Elevation loss:')
        # self.distance_value = QtWidgets.QLabel(str(round(self.summary.distance / 1000, 2)))
        # self.distance_unit = QtWidgets.QLabel('km')

        self.layout.addWidget(self.title, 0, 0, 1, 3)

        self.layout.addWidget(self.distance, 1, 0)
        self.layout.addWidget(self.distance_value, 1, 1)
        self.layout.addWidget(self.distance_unit, 1, 2)

        self.layout.addWidget(self.elevation_gain, 2, 0)
        self.layout.addWidget(self.elevation_gain_value, 2, 1)
        self.layout.addWidget(self.elevation_gain_unit, 2, 2)

        self.layout.addWidget(self.duration, 3, 0)
        self.layout.addWidget(self.duration_value, 3, 1)
        self.layout.addWidget(self.duration_unit, 3, 2)


class ActivityInfobox(InfoWidget):

    def __init__(self, activity, parent=None):
        super(ActivityInfobox, self).__init__(parent)

        self.activity = activity

        if not activity:
            return

        # self.title = QtWidgets.QLabel(self.activity.name)
        # self.title.setAlignment(QtCore.Qt.AlignCenter)
        # self.title.setWordWrap(True)
        # self.title.setFont(self.title_font)

        self.title.setText(self.activity.name)

        self.date = QtWidgets.QLabel('Date:')
        self.date_value = QtWidgets.QLabel(str(self.activity.date))

        self.distance = QtWidgets.QLabel('Distance:')
        self.distance_value = QtWidgets.QLabel(str(round(self.activity[ActivityInfo.Distance] / 1000, 2)))
        self.distance_unit = QtWidgets.QLabel('km')

        self.elevation_gain = QtWidgets.QLabel('Elevation gain:')
        self.elevation_gain_value = QtWidgets.QLabel(str(round(self.activity[ActivityInfo.ElevationGain], 2)))
        self.elevation_gain_unit = QtWidgets.QLabel('m')

        self.duration = QtWidgets.QLabel('Duration:')
        self.duration_value = QtWidgets.QLabel(format_seconds_to_hhmmss(self.activity[ActivityInfo.Duration]))
        self.duration_unit = QtWidgets.QLabel('')

        self.layout.addWidget(self.title, 0, 0, 1, 3)

        self.layout.addWidget(self.date, 1, 0)
        self.layout.addWidget(self.date_value, 1, 1)

        self.layout.addWidget(self.distance, 2, 0)
        self.layout.addWidget(self.distance_value, 2, 1)
        self.layout.addWidget(self.distance_unit, 2, 2)

        self.layout.addWidget(self.elevation_gain, 3, 0)
        self.layout.addWidget(self.elevation_gain_value, 3, 1)
        self.layout.addWidget(self.elevation_gain_unit, 3, 2)

        self.layout.addWidget(self.duration, 4, 0)
        self.layout.addWidget(self.duration_value, 4, 1)
        self.layout.addWidget(self.duration_unit, 4, 2)





def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


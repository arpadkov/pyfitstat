from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from pyfitstat.model.model import ViewType
from activity_sorter import ActivitySorter, PlotCreator
from plot_widget import PlotWidget
from top_row import TopRow
from bottom_row import BottomRow

import datetime
import monthdelta


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, activities, parent=None):
        super(MainWindow, self).__init__(parent)

        self.activities = activities

        self.view_type = ViewType.All

        self.act_types = ['Running', 'Cycling', 'Hiking']
        self.act_type = self.act_types[0]

        self.act_info = 'distance'

        self.year = datetime.date.today().year
        self.month = datetime.date.today().month

        self.sorter = ActivitySorter(self.activities)
        self.plotter = PlotCreator(self.sorter, self.view_type, self.act_type, self.act_info, self.year, self.month)
        self.plot_data = None
        self.info_widget = None

        layout = QtWidgets.QVBoxLayout()

        self.plot_widget = PlotWidget(parent=self)

        self.top_row = TopRow(parent=self)
        self.top_row.data_changed.connect(self.plot)
        self.top_row.act_type_change.connect(self.act_type_changed)
        self.top_row.view_type_change.connect(self.view_type_changed)
        # self.top_row.calender_left.connect(self.calender_left)
        # self.top_row.calender_right.connect(self.calender_right)
        self.top_row.calender_change.connect(self.calender_change)

        self.bottom_row = BottomRow(parent=self)
        # self.top_row.data_changed.connect(self.plot)

        layout.addWidget(self.top_row)
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.bottom_row)

        window = QtWidgets.QWidget()
        window.setLayout(layout)  # set layout to our central widget
        self.setCentralWidget(window)  # set w as central widget

    def _on_data_change(self):
        # self.sorter = ActivitySorter(self.activities, self.view_type, self.act_type, self.act_info, self.year,
        #                              self.month)
        self.plotter = PlotCreator(self.sorter, self.view_type, self.act_type, self.act_info, self.year, self.month)
        # self.current_activities = self.sorter.get_activities(self.view_type, self.year, self.month)
        # self.plot()

    def plot(self):
        self._on_data_change()
        self.plot_data = self.plotter.create_plot_data()
        self.plot_widget.plot(self.plot_data)

    def keyPressEvent(self, event) -> None:
        print(event.key())

    def view_type_changed(self, view_type):

        self.view_type = view_type
        if self.view_type is ViewType.All:
            self.year = datetime.date.today().year
            self.month = datetime.date.today().month

    def act_type_changed(self, act_type):
        self.act_type = act_type

    def calender_change(self, step):

        if self.view_type is ViewType.Year:
            self.year_step(step)
        elif self.view_type is ViewType.Month:
            self.month_step(step)

    def year_step(self, step: int):

        date_min = datetime.date(self.year + step, 1, 5)
        date_max = datetime.date(self.year + step, 12, 5)

        if self.date_is_valid(date_min) or self.date_is_valid(date_max):
            self.year += step

    def month_step(self, step: int):

        date = datetime.date(self.year, self.month, 5) + monthdelta.monthdelta(step)
        if self.date_is_valid(date):
            self.year = date.year
            self.month = date.month

    def date_is_valid(self, date: datetime.date):

        max_date = datetime.date(max(self.plotter.act_years()), self.plotter.last_month(), 28)
        min_date = datetime.date(min(self.plotter.act_years()), self.plotter.first_month(), 1)

        return True if min_date < date < max_date else False

    def artist_clicked(self, event):

        if self.view_type is ViewType.All:
            self.year_clicked(num=event.artist.get_gid())
        elif self.view_type is ViewType.Year:
            self.month_clicked(num=event.artist.get_gid())
        elif self.view_type is ViewType.Month:
            self.day_clicked(num=event.artist.get_gid())

    def year_clicked(self, num):
        self.year = self.plotter.act_years()[num]
        self.view_type = ViewType.Year
        self.plot()

    def month_clicked(self, num):
        self.month = num+1
        self.view_type = ViewType.Month
        self.plot()

    def day_clicked(self, num):
        print(num+1)

    def show_popup(self, event):

        # print(self.frameGeometry())
        # print(self.plot_widget.frameGeometry().center())
        pass
        # self.info_widget = InfoWidget(parent=self)
        # self.info_widget.setGeometry(100, 100, 100, 100)
        # self.info_widget.show()
        # print(self.info_widget)

    def artist_hover_in(self, event):

        if event.inaxes == self.plot_widget.ax:

            for bar, annot in zip(self.plot_widget.bars, self.plot_widget.annotations):
                cont, ind = bar.patches[0].contains(event)

                if cont:

                    # ==================================================================================================

                    rect_xy = bar.patches[0].get_xy()

                    rect_center_x = rect_xy[0] + bar.patches[0].get_width()/2
                    rect_center_y = rect_xy[1] + bar.patches[0].get_height()/2

                    xy_pixels = self.plot_widget.ax.transData.transform((rect_center_x, rect_center_y))
                    print(xy_pixels)



                    # ==================================================================================================

                    annot.set_visible(True)
                else:
                    annot.set_visible(False)
            self.plot_widget.canvas.draw()

    def mouse_left(self, event):

        # self.info_widget.hide()

        for annot in self.plot_widget.annotations:
            annot.set_visible(False)
            self.plot_widget.canvas.draw()

    def show_distance(self):
        self.act_info = 'distance'
        self.plot()

    def show_duration(self):
        self.act_info = 'duration'
        self.plot()

    def show_elevation_gain(self):
        self.act_info = 'elevation_gain'
        self.plot()

    def show_elevation_loss(self):
        self.act_info = 'elevation_loss'
        self.plot()








from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from activity_sorter import ActivitySorter, PlotCreator
from plot_widget import PlotWidget
from top_row import TopRow
from bottom_row import BottomRow
import datetime
from infobox_widget import InfoWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, activities, parent=None):
        super(MainWindow, self).__init__(parent)

        # self.activities = activities
        # self.current_activities = self.activities
        #
        # self.current_view = 'All'
        # self.current_year = max(self.years)
        # self.current_month = 3
        # self.current_type = 'Running'
        # self.current_info = 'distance'

        self.activities = activities
        # self.current_activities = []

        self.view_types = ['All', 'Year', 'Month']
        self.view_type = self.view_types[0]

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
        self.bottom_row = BottomRow(parent=self)

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

    def view_type_changed(self):

        self.view_type = self.top_row.cb_calender.currentText()
        if self.view_type == 'All':
            self.year = datetime.date.today().year
            self.month = datetime.date.today().month
        self.plot()

    def act_type_changed(self):

        self.act_type = self.top_row.cb_activity_type.currentText()
        self.plot()

    def right_click(self):

        if self.view_type == 'All':
            return

        if self.view_type == 'Year':

            if self.year == max(self.plotter.act_years()):
                pass
            else:
                self.year += 1

        if self.view_type == 'Month':

            if self.month == 12 and self.year == max(self.plotter.act_years()):
                pass
            elif self.month == 12:
                self.month = 1
                self.year += 1
            else:
                self.month += 1

        self.plot()

    def left_click(self):

        if self.view_type == 'All':
            return

        if self.view_type == 'Year':

            if self.year == min(self.plotter.act_years()):
                pass
            else:
                self.year -= 1

        if self.view_type == 'Month':

            if self.month == 1 and self.year == min(self.plotter.act_years()):
                pass
            elif self.month == 1:
                self.month = 12
                self.year -= 1
            else:
                self.month -= 1

        self.plot()

    def artist_clicked(self, event):

        actions = {
            self.view_types[0]: self.year_clicked,
            self.view_types[1]: self.month_clicked,
            self.view_types[2]: self.day_clicked,
        }

        actions[self.view_type](num=event.artist.get_gid())

    def year_clicked(self, num):
        self.year = self.plotter.act_years()[num]
        self.view_type = 'Year'
        self.plot()

    def month_clicked(self, num):
        self.month = num+1
        self.view_type = 'Month'
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







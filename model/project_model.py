from pyfitstat.model.plot_data import PlotData, AllPlot, YearPlot, MonthPlot

from PyQt5.QtCore import QObject, pyqtSignal

from enum import Enum
import datetime
import monthdelta


class ViewType(Enum):

    All = 1
    Year = 2
    Month = 3


class ActivityType(Enum):

    Running = 1
    Cycling = 2
    Hiking = 3


class ActivityInfo(Enum):

    Distance = 1
    Duration = 2
    ElevationGain = 3
    ElevationLoss = 4


class MessageObject(QObject):

    selection_changed = pyqtSignal()

    def __init__(self):
        super(MessageObject, self).__init__()

    def emit_selection_change(self):
        self.selection_changed.emit()


class ActivityModel:

    def __init__(self, activities):
        self.message_obj = MessageObject()

        self.activities = activities

        self.view_type = ViewType.All
        self.act_type = ActivityType.Running
        self.act_info = ActivityInfo.Distance

        self.year = datetime.date.today().year
        self.month = datetime.date.today().month

    @property
    def plot_data(self):

        plots = {
            ViewType.All: AllPlot,
            ViewType.Year: YearPlot,
            ViewType.Month: MonthPlot
        }

        return plots.get(self.view_type)(
            self.activities,
            self.view_type,
            self.act_type,
            self.act_info,
            self.year,
            self.month
        )

    @property
    def last_year(self):
        return self.activities[-1].date.year

    @property
    def first_year(self):
        return self.activities[0].date.year

    @property
    def last_month(self):
        return self.activities[-1].date.month

    @property
    def first_month(self):
        return self.activities[0].date.month

    def calendar_change(self, step):

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

        max_date = datetime.date(self.last_year, self.last_month, 28)
        min_date = datetime.date(self.first_year, self.first_month, 1)

        return True if min_date < date < max_date else False

    def plot_clicked(self, num):

        if self.view_type is ViewType.All:
            self.year = self.plot_data.act_years()[num]
            self.view_type = ViewType.Year

        elif self.view_type is ViewType.Year:
            self.month = num + 1
            self.view_type = ViewType.Month

        elif self.view_type is ViewType.Month:
            print(num+1)

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)

        self.message_obj.emit_selection_change()

from pyfitstat.model.sorter import ActivitySorter
from pyfitstat.gui.GUIInfoboxWidget import InfoWidget

import datetime
import calendar


class PlotData:

    def __init__(self, activities, view_type, act_type, act_info, year, month):

        self.activities = activities

        self.view_type = view_type
        self.act_type = act_type
        self.act_info = act_info

        self.year = year
        self.month = month

        self.create_title()
        self.create_labels()
        self.create_values()

        # self.create_annotations()

    def act_years(self):
        return [i for i in range(self.activities[0].year, self.activities[-1].year + 1)]

    @staticmethod
    def act_months():
        return [datetime.date(1, i + 1, 1).strftime("%b") for i in range(12)]


class AllPlot(PlotData):

    def __init__(self, *args, **kwargs):
        super(AllPlot, self).__init__(*args, **kwargs)

    def create_title(self):
        self.title = f'{self.act_type.name} - All'

    def create_labels(self):
        self.labels = [str(label) for label in self.act_years()]

    def create_values(self):

        self.values = []
        for year in self.act_years():
            year_sorter = ActivitySorter(self.activities, self.act_type, year)
            year_acts = year_sorter.get_activities()
            self.values.append(sum([act.data(self.act_info) for act in year_acts]))

    def create_annotations(self):

        self.annotations = []
        for value in self.values:
            info_widget = InfoWidget(label=str(value))
            self.annotations.append(info_widget)


class YearPlot(PlotData):

    def __init__(self, *args, **kwargs):
        super(YearPlot, self).__init__(*args, **kwargs)

    def create_title(self):
        self.title = f'{self.act_type.name} - {self.year}'

    def create_labels(self):
        self.labels = self.act_months()

    def create_values(self):

        self.values = []
        for month in range(len(self.act_months())):
            month_sorter = ActivitySorter(self.activities, self.act_type, self.year, month+1)
            month_acts = month_sorter.get_activities()
            self.values.append(sum([act.data(self.act_info) for act in month_acts]))

    def create_annotations(self):

        self.annotations = []
        for value in self.values:
            info_widget = InfoWidget(label=str(value))
            self.annotations.append(info_widget)


class MonthPlot(PlotData):

    def __init__(self, *args, **kwargs):
        super(MonthPlot, self).__init__(*args, **kwargs)

    def create_title(self):
        self.title = f'{self.act_type.name} - {self.year} {self.act_months()[self.month-1]}'

    def create_labels(self):
        days = calendar.monthrange(self.year, self.month)[1]
        self.labels = [i + 1 for i in range(days)]

    def create_values(self):

        self.values = [0] * len(self.labels)

        month_sorter = ActivitySorter(self.activities, self.act_type, self.year, self.month)
        month_acts = month_sorter.get_activities()

        for day in self.labels:

            day_acts = []

            for act in month_acts:
                if act.date.day == day:
                    day_acts.append(act)

            self.values[day-1] = sum([act.data(self.act_info) for act in day_acts])

    def create_annotations(self):

        self.annotations = []
        for value in self.values:
            info_widget = InfoWidget(label=str(value))
            self.annotations.append(info_widget)

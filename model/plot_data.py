from pyfitstat.model.sorter import ActivitySorter
from pyfitstat.model.activity import ViewType, ActivityType, ActivityInfo

import datetime
import calendar


class PlotData:

    def __init__(self, activities, first_year, last_year, view_type, act_type, act_info, year, month):

        self.activities = activities

        self.first_year = first_year
        self.last_year = last_year

        self.view_type = view_type
        self.act_type = act_type
        self.act_info = act_info

        self.year = year
        self.month = month

        self.create_title()
        if self.first_year and self.last_year:
            self.create_labels()
            self.create_values()
            self.format_data()

    def create_title(self):
        raise NotImplementedError

    def create_labels(self):
        raise NotImplementedError

    def create_values(self):
        raise NotImplementedError

    def format_data(self):

        if self.act_info == ActivityInfo.Distance:
            self.values = [x/1000 for x in self.values]
            self.y_label = 'km'

    def act_years(self):
        return [i for i in range(self.first_year, self.last_year + 1)]

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
        self.summaries = []

        for year in self.act_years():
            year_sorter = ActivitySorter(self.activities, self.act_type, year)
            year_acts = year_sorter.get_activities()

            summary_title = f'{year}'
            self.values.append(sum([act[self.act_info] for act in year_acts]))
            self.summaries.append(ActivityListSummary(summary_title, year_acts))







class YearPlot(PlotData):

    def __init__(self, *args, **kwargs):
        super(YearPlot, self).__init__(*args, **kwargs)

    def create_title(self):
        self.title = f'{self.act_type.name} - {self.year}'

    def create_labels(self):
        self.labels = self.act_months()

    def create_values(self):

        self.values = []
        self.summaries = []

        for month in range(len(self.act_months())):
            month_sorter = ActivitySorter(self.activities, self.act_type, self.year, month+1)
            month_acts = month_sorter.get_activities()
            self.values.append(sum([act[self.act_info] for act in month_acts]))

            summary_title = f'{self.act_months()[month]}'
            self.summaries.append(ActivityListSummary(summary_title, month_acts))


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
        self.summaries = [None] * len(self.labels)

        month_sorter = ActivitySorter(self.activities, self.act_type, self.year, self.month)
        month_acts = month_sorter.get_activities()

        for day in self.labels:

            day_acts = []

            for act in month_acts:
                if act.date.day == day:
                    day_acts.append(act)

            self.values[day-1] = sum([act[self.act_info] for act in day_acts])
            if len(day_acts):

                distances = [act[ActivityInfo.Distance] for act in day_acts]
                main_distance = max(distances)
                main_index = distances.index(main_distance)

                self.summaries[day-1] = day_acts[main_index]


class ActivityListSummary:

    def __init__(self, title, activities):

        self.title = title
        self.activities = activities

    @property
    def distance(self):
        return sum([act[ActivityInfo.Distance] for act in self.activities])

    @property
    def duration(self):
        return sum([act[ActivityInfo.Duration] for act in self.activities])

    @property
    def elevation_gain(self):
        return sum([act[ActivityInfo.ElevationGain] for act in self.activities])

    @property
    def elevation_loss(self):
        return sum([act[ActivityInfo.ElevationLoss] for act in self.activities])



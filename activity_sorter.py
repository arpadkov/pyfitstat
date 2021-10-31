import datetime
import calendar


class ActivitySorter:

    def __init__(self, activities):

        self.activities = activities

        # self.view_type = view_type
        # self.act_type = act_type
        # self.act_info = act_info
        #
        # self.year = year
        # self.month = month

    def get_activities(self, view_type, act_type, year=None, month=None):
        if view_type == 'All':
            return self.get_all(act_type)

        elif view_type == 'Year':
            return self.get_yearly(year, act_type)

        elif view_type == 'Month':
            return self.get_monthly(year, month, act_type)

    def get_all(self, act_type):

        acts = []

        for act in self.activities:
            if act.act_type == act_type:
                acts.append(act)

        return acts

    def get_yearly(self, year, act_type):
        acts = []

        for act in self.activities:
            if act.date.year == year and act.act_type == act_type:
                acts.append(act)

        return acts

    def get_monthly(self, year, month, act_type):
        acts = []

        for act in self.activities:
            if act.date.year == year and act.date.month == month:
                acts.append(act)

        return acts


class PlotCreator:

    def __init__(self, sorter, view_type, act_type, act_info, year, month):

        self.sorter = sorter

        self.view_type = view_type
        self.act_type = act_type
        self.act_info = act_info

        self.year = year
        self.month = month

    def create_plot_data(self):
        plot_data = {
            "title": self.create_title(),
            "labels": self.create_labels(),
            "values": self.create_values(),
            "act_info": self.act_info
        }

        return plot_data

    def create_title(self):
        titles = {
            "All": f'{self.act_type} - All',
            "Year": f'{self.act_type} - {self.year}',
            "Month": f'{self.act_type} - {self.year} {self.act_months()[self.month-1]}'
        }

        return titles[self.view_type]

    def create_labels(self):
        labels = {
            "All": self.get_labels_all,
            "Year": self.get_labels_year,
            "Month": self.get_labels_month,
        }

        return labels[self.view_type]()

    def get_labels_all(self):
        return self.act_years()

    def get_labels_year(self):
        return self.act_months()

    def get_labels_month(self):
        days = calendar.monthrange(self.year, self.month)[1]
        return [i+1 for i in range(days)]

    def create_values(self):
        values = {
            "All": self.get_values_all,
            "Year": self.get_values_year,
            "Month": self.get_values_month,
        }

        return values[self.view_type]()

    def get_values_all(self):

        values = []

        for year in self.act_years():
            acts = self.sorter.get_activities('Year', self.act_type, year)
            values.append(sum([act.data[self.act_info] for act in acts]))

        return values

    def get_values_year(self):

        values = []

        for month in range(len(self.act_months())):
            acts = self.sorter.get_activities('Month', self.act_type, self.year, month+1)
            values.append(sum([act.data[self.act_info] for act in acts]))

        return values

    def get_values_month(self):

        days = self.get_labels_month()
        values = [0] * len(days)

        acts = self.sorter.get_activities('Month', self.act_type, self.year, self.month)

        for day in days:

            day_acts = []

            for act in acts:
                if act.date.day == day:
                    day_acts.append(act)

            values[day-1] = sum([act.data[self.act_info] for act in day_acts])

        return values

    def act_years(self):
        return [i for i in range(self.sorter.activities[0].year, self.sorter.activities[-1].year + 1)]

    @staticmethod
    def act_months():
        return [datetime.date(1, i + 1, 1).strftime("%b") for i in range(12)]





class ActivitySorter:

    def __init__(self, activities, act_type, year=None, month=None):

        self.activities = activities
        self.act_type = act_type
        self.year = year
        self.month = month

        self.sorted_activities = []

    def get_activities(self):

        if self.year and self.month:
            self.get_monthly()

        elif self.year:
            self.get_yearly()

        else:
            self.get_all()

        return self.sorted_activities

    def get_all(self):

        for act in self.activities:
            if act.act_type == self.act_type:
                self.sorted_activities.append(act)

    def get_yearly(self):

        for act in self.activities:
            if act.date.year == self.year and act.act_type == self.act_type:
                self.sorted_activities.append(act)

    def get_monthly(self):

        for act in self.activities:
            if act.date.year == self.year and act.date.month == self.month and act.act_type == self.act_type:
                self.sorted_activities.append(act)

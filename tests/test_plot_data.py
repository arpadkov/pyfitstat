from pyfitstat.model.activity import Activity

from PyQt5 import QtWidgets

import unittest
import logging
import os


class TestWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(TestWidget, self).__init__(parent)


def create_activities(wd):
    activities = []
    for activity_name in os.listdir(wd)[0:100]:
        if '.json' in activity_name:

            try:
                activity = Activity.read_from_json(os.path.join(wd, activity_name))
                activities.append(activity)
            except Exception as ex:
                logging.warning(f'Activity {activity_name} is corrupted: {ex}')
    return activities


class PlotDataTest(unittest.TestCase):

    def test_plot_data(self):

        # activities = create_activities(os.path.join(os.getenv('APPDATA'), 'pyfitstat', 'bontovics.t@gmail.com'))

        test_annot = TestWidget()

        print(test_annot)

        # all_plot = AllPlot(activities=activities,
        #                    view_type=ViewType.All,
        #                    act_type=ActivityType.Running,
        #                    act_info=ActivityInfo.Distance,
        #                    year=2,
        #                    month=2)




if __name__ == '__main__':
    unittest.main()




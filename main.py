from pyfitstat.model.activity import Activity
from pyfitstat.model.project_model import ActivityModel
from pyfitstat.gui.main_window import MainWindow

from PyQt5 import QtWidgets, QtCore
from garminexport.incremental_backup import incremental_backup

import os
import sys
import logging
import json
import time


logging.basicConfig(level='INFO')


class FitnessApp:

    def __init__(self, username=None, password=None, sync=True, wd=None):

        self.username = username
        self.password = password
        self._sync = sync
        self._wd = wd




    def on_start(self):

        self.get_user_data()

        self.check_backup_dir()



        # if self._sync:
        #     self.sync_data()

    def get_user_data(self):

        if not os.path.exists(os.path.join(os.getenv('APPDATA'), 'pyfitstat')):
            os.makedirs(os.path.join(os.getenv('APPDATA'), 'pyfitstat'))

        if self.username is None:
            self.read_user_data()

        if self.username is None:
            self.prompt_user_data()

    def read_user_data(self):

        if os.path.isfile(os.path.join(os.getenv('APPDATA'), 'pyfitstat', 'users.json')):

            with open(os.path.join(os.getenv('APPDATA'), 'pyfitstat', 'users.json')) as file:
                json_data = json.load(file)
                self.username = json_data["default"]
                self.password = json_data[self.username]

    def prompt_user_data(self):

        self.username = input('Username:')
        self.password = input(f"Enter password for {self.username}: ")
        save_user = int(input('Save user? (Yes=1, No=0)'))

        if save_user:
            self.save_user_data()

    def save_user_data(self):

        if os.path.isfile(os.path.join(os.getenv('APPDATA'), 'pyfitstat', 'users.json')):
            with open(os.path.join(os.getenv('APPDATA'), 'pyfitstat', 'users.json')) as file:
                json_data = json.load(file)
        else:
            json_data = {}

        json_data[self.username] = self.password
        json_data["default"] = self.username

        with open(os.path.join(os.getenv('APPDATA'), 'pyfitstat', 'users.json'), 'w') as file:
            json.dump(json_data, file, indent=4)

    def open_window(self):

        # model = ActivityModel(self.create_activities())
        self.on_start()
        app = QtWidgets.QApplication(sys.argv)
        self.main_window = MainWindow(ActivityModel(
            username=self.username,
            password=self.password,
            wd=self._wd,
            activities=[]
        ))
        # self.main_window.show()

        # self.main_window.model.sync_activities()
        # self.main_window.model.create_activities()

        if self._sync:
            self.main_window.model.sync_activities()

        else:
            self.main_window.model.create_activities()


        #
        # self.main_window.update_model(ActivityModel(self.create_activities()))
        #
        # self.main_window.plot_widget.plot()

        sys.exit(app.exec_())

    def check_backup_dir(self):

        backup_dir = os.path.join(os.getenv('APPDATA'), 'pyfitstat', self.username)

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        self._wd = backup_dir

    # def sync_data(self):
    #
    #     incremental_backup(
    #         username=self.username,
    #         password=self.password,
    #         backup_dir=self._wd,
    #         export_formats=['json_summary'],
    #         ignore_errors=False,
    #         max_retries=7
    #     )

    # def create_activities(self):
    #
    #     acts = []
    #
    #     for activity_name in os.listdir(self._wd):
    #         if '.json' in activity_name:
    #
    #             try:
    #                 activity = Activity.read_from_json(os.path.join(self._wd, activity_name))
    #                 acts.append(activity)
    #             except Exception as ex:
    #                 logging.warning(f'Activity {activity_name} is corrupted: {ex}')
    #
    #     return acts

def main():
    fitness_app = FitnessApp(sync=True)
    fitness_app.open_window()


if __name__ == "__main__":
    main()



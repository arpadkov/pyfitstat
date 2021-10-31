# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 20:24:39 2021

@author: 95arp
"""
import json
import getpass

from garminexport import incremental_backup
from activity import Activity
from activity_sorter import ActivitySorter
from main_window import MainWindow

from PyQt5 import QtWidgets

import os
import sys
import datetime
import logging

logging.basicConfig(level='ERROR')




class FitnessApp:

    def __init__(self, username=None, password=None, sync=True, wd=None):

        self.username = username
        self.password = password
        self._sync = sync
        self._wd = wd

        self.activities = []
        # # self.current_activities = []
        #
        # self.view_types = ['All', 'Year', 'Month']
        # self.view_type = self.view_types[0]
        #
        # self.act_types = ['Running', 'Cycling', 'Hiking']
        # self.act_type = self.act_types[0]
        #
        # self.act_info = 'distance'
        #
        # self.year = datetime.date.today().year
        # self.month = datetime.date.today().month

        self.main_window = None

        self.on_start()

        # self.sorter = ActivitySorter(self.activities, self.view_type, self.act_type, self.act_info, self.year, self.month)

    def on_start(self):

        self.get_user_data()

        self.check_backup_dir()

        if self._sync:
            self.sync_data()

        self.create_activities()

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

        app = QtWidgets.QApplication(sys.argv)
        self.main_window = MainWindow(self.activities)
        self.main_window.show()
        # setattr(self.main_window, 'activities', self.activities)
        self.main_window.plot()
        sys.exit(app.exec_())

    def check_backup_dir(self):

        backup_dir = os.path.join(os.getenv('APPDATA'), 'pyfitstat', self.username)

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        self._wd = backup_dir

        # if self._wd is None:
        #     cwd = os.getcwd()
        #
        #     backup_dir = os.path.join(cwd, self.username)
        #     self._wd = backup_dir


    def sync_data(self):

        incremental_backup.incremental_backup(
            username=self.username,
            password=self.password,
            backup_dir=self._wd,
            export_formats=['json_summary'],
            ignore_errors=False,
            max_retries=7
        )

    def create_activities(self):

        for activity_name in os.listdir(self._wd):
            if '.json' in activity_name:

                try:
                    activity = Activity.read_from_json(os.path.join(self._wd, activity_name))
                    self.activities.append(activity)
                except Exception as ex:
                    logging.warning(f'Activity {activity_name} is corrupted: {ex}')

    # def _on_data_change(self):
    #     self.sorter = ActivitySorter(self.activities, self.view_type, self.act_type)
    #     self.refresh_current_activities()
    #     self.main_window.plot(plot_data=self.sorter.create_plot_data())

    # def refresh_current_activities(self):
    #     self.current_activities = self.sorter.get_activities(self.year, self.month)



def main():
    fitness_app = FitnessApp(sync=False)
    fitness_app.open_window()



if __name__ == "__main__":
    main()



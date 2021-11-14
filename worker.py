from PyQt5 import QtWidgets, QtCore
from garminexport.incremental_backup import incremental_backup

import logging

logger = logging.getLogger('pyfitstat')


class Worker(QtCore.QObject):

    finished = QtCore.pyqtSignal()

    def __init__(self, username, password, wd):
        super(Worker, self).__init__()

        self.username = username
        self.password = password
        self._wd = wd

    def run(self):
        self.sync_data()
        self.finished.emit()

    def sync_data(self):

        try:
            incremental_backup(
                username=self.username,
                password=self.password,
                backup_dir=self._wd,
                export_formats=['json_summary'],
                ignore_errors=False,
                max_retries=7
            )
        except Exception as ex:
            logger.error('Server not responding')


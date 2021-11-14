from pyfitstat.model.activity import Activity

from garminexport.incremental_backup import incremental_backup

import logging
import datetime
import os


logging.basicConfig(level='INFO')

username = '95.arpadkov@gmail.com'
password = 'Emiatyuk95'

cwd = os.getcwd()

backup_dir = os.path.join(cwd, username)
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)


incremental_backup(
            username=username,
            password=password,
            backup_dir=os.path.join(cwd, username),
            export_formats=['json_summary'],
            ignore_errors=False,
            max_retries=7
            )

activities = []
for activity_name in os.listdir(backup_dir):
    if '.json' in activity_name:

        try:
            activity = Activity.read_from_json(os.path.join(backup_dir, activity_name))
            activities.append(activity)
        except Exception as ex:
            logging.warning(f'Activity {activity_name} is corrupted: {ex}')

td = datetime.timedelta(seconds=activities[-1]._moving_duration)
print(td)

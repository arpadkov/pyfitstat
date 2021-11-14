from enum import Enum
import json
import logging
import datetime

logger = logging.getLogger('pyfitstat')

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


class Activity:
    
    def __init__(self, act_id, raw_data):
        
        self.act_id = act_id
        self.raw_data = raw_data
        
        self._name = raw_data['activityName']

        self._date = raw_data['summaryDTO']['startTimeLocal']

        self.distance = float(raw_data['summaryDTO']['distance'])
        self.elevation_gain = float(raw_data['summaryDTO']['elevationGain'])
        self.elevation_loss = float(raw_data['summaryDTO']['elevationLoss'])
        self.max_elevation = float(raw_data['summaryDTO']['maxElevation'])
        self.min_elevation = float(raw_data['summaryDTO']['minElevation'])

        self._moving_duration = raw_data['summaryDTO']['movingDuration']
        self._elapsed_duration = raw_data['summaryDTO']['elapsedDuration']

        self._type = raw_data['activityTypeDTO']['typeKey']
        
    @classmethod
    def read_from_json(cls, filename):
        
        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        
        act_id = json_data['activityId']
        act_date = json_data['summaryDTO']['startTimeLocal'][0:10]

        try:
            return cls(act_id, json_data)
        except Exception as ex:
            logger.warning(f'Activity {act_date} is corrupted: {ex}')

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return 'Unnamed activity'

    @property
    def date(self):

        date_list = self._date[0:10].split('-')

        year = int(date_list[0])
        month = int(date_list[1])
        day = int(date_list[2])

        date = datetime.date(year, month, day)

        return date

    @property
    def act_type(self):

        if 'running' in self._type or 'other' in self._type or 'walking' in self._type:
            return ActivityType.Running
        else:
            return ActivityType[self._type.capitalize()]

    @property
    def duration(self):
        return self._moving_duration

    @property
    def year(self):
        return int(self.date.year)

    @property
    def month(self):
        return self.date.strftime('%b')

    @property
    def day(self):
        return int(self.date.day)

    def data(self, info):

        activity_data = {
            ActivityInfo.Distance: self.distance,
            ActivityInfo.ElevationGain: self.elevation_gain,
            ActivityInfo.ElevationLoss: self.elevation_loss,
            "max_elevation": self.max_elevation,
            "min_elevation": self.min_elevation,
            "type": self.act_type,
            "date": self.date,
            ActivityInfo.Duration: self.duration
        }

        return activity_data.get(info)

    def __lt__(self, other):
        return self.date < other.date

        
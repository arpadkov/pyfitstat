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

    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__


class ActivityInfo(Enum):

    Distance = 1
    Duration = 2
    ElevationGain = 3
    ElevationLoss = 4


class Activity:

    def __init__(self, json_data):

        self._json_data = json_data

    @classmethod
    def read_from_json(cls, filename):

        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        return cls(json_data)

    @property
    def act_id(self):
        return self._json_data['activityId']

    @property
    def name(self):
        if self._json_data['activityName']:
            return self._json_data['activityName'].replace('Nicht klassifiziert', '')
        else:
            return 'Unnamed activity'

    @property
    def date(self):

        year, month, day = tuple(self._json_data['summaryDTO']['startTimeLocal'][0:10].split('-'))

        return datetime.date(int(year), int(month), int(day))

    @property
    def act_type(self):

        act_type_str = self._json_data['activityTypeDTO']['typeKey']

        if ActivityType.has_member_key( act_type_str.capitalize()):
            return ActivityType[act_type_str.capitalize()]
        else:
            return ActivityType.Running

    def distance(self):
        return float(self._json_data['summaryDTO']['distance'])

    def elevation_gain(self):
        return float(self._json_data['summaryDTO']['elevationGain'])

    def elevation_loss(self):
        return float(self._json_data['summaryDTO']['elevationLoss'])

    def duration(self):
        return float(self._json_data['summaryDTO']['movingDuration'])

    def data(self, info: ActivityInfo):

        activity_data = {
            ActivityInfo.Distance: self.distance,
            ActivityInfo.ElevationGain: self.elevation_gain,
            ActivityInfo.ElevationLoss: self.elevation_loss,
            ActivityInfo.Duration: self.duration
        }

        try:
            return activity_data.get(info)()
        except Exception as ex:
            logger.warning(f'Activity {self.date} is missing: {ex}')
            return 0

    def __getitem__(self, key: ActivityInfo):
        return self.data(key)

    def __repr__(self):
        return f'{self.name} - {self.date}'


# class AActivity:
#
#     def __init__(self, act_id, raw_data):
#
#         self.act_id = act_id
#         self.raw_data = raw_data
#
#         self._name = raw_data['activityName']
#
#         self._date = raw_data['summaryDTO']['startTimeLocal']
#
#         self.distance = float(raw_data['summaryDTO']['distance'])
#         self.elevation_gain = float(raw_data['summaryDTO']['elevationGain'])
#         self.elevation_loss = float(raw_data['summaryDTO']['elevationLoss'])
#         self.max_elevation = float(raw_data['summaryDTO']['maxElevation'])
#         self.min_elevation = float(raw_data['summaryDTO']['minElevation'])
#
#         self._moving_duration = raw_data['summaryDTO']['movingDuration']
#         self._elapsed_duration = raw_data['summaryDTO']['elapsedDuration']
#
#         self._type = raw_data['activityTypeDTO']['typeKey']
#
#     @classmethod
#     def read_from_json(cls, filename):
#
#         with open(filename, 'r', encoding='utf-8') as file:
#             json_data = json.load(file)
#
#         act_id = json_data['activityId']
#         act_date = json_data['summaryDTO']['startTimeLocal'][0:10]
#
#         try:
#             return cls(act_id, json_data)
#         except Exception as ex:
#             logger.warning(f'Activity {act_date} is corrupted: {ex}')
#
#     @property
#     def name(self):
#         if self._name:
#             return self._name
#         else:
#             return 'Unnamed activity'
#
#     @property
#     def date(self):
#
#         date_list = self._date[0:10].split('-')
#
#         year = int(date_list[0])
#         month = int(date_list[1])
#         day = int(date_list[2])
#
#         date = datetime.date(year, month, day)
#
#         return date
#
#     @property
#     def act_type(self):
#
#         if 'running' in self._type or 'other' in self._type or 'walking' in self._type:
#             return ActivityType.Running
#         else:
#             return ActivityType[self._type.capitalize()]
#
#     @property
#     def duration(self):
#         return self._moving_duration

    # @property
    # def year(self):
    #     return int(self.date.year)
    #
    # @property
    # def month(self):
    #     return self.date.strftime('%b')
    #
    # @property
    # def day(self):
    #     return int(self.date.day)

    # def data(self, info):
    #
    #     activity_data = {
    #         ActivityInfo.Distance: self.distance,
    #         ActivityInfo.ElevationGain: self.elevation_gain,
    #         ActivityInfo.ElevationLoss: self.elevation_loss,
    #         "max_elevation": self.max_elevation,
    #         "min_elevation": self.min_elevation,
    #         "type": self.act_type,
    #         "date": self.date,
    #         ActivityInfo.Duration: self.duration
    #     }
    #
    #     return activity_data.get(info)
    #
    # def __lt__(self, other):
    #     return self.date < other.date

        
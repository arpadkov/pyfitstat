# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 20:19:40 2021

@author: 95arp
"""

import json
import datetime


class Activity:
    
    def __init__(self, act_id, raw_data):
        
        self.act_id = act_id
        self.raw_data = raw_data
        
        self.name = raw_data['activityName']

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
            raw = json.load(file)
        
        act_id = raw['activityId']

        return cls(act_id, raw)

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

        if 'running' in self._type or 'other' in self._type:
            return 'Running'
        else:
            return self._type.capitalize()

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

    @property
    def data(self):
        return {
            "distance": self.distance,
            "elevation_gain": self.elevation_gain,
            "elevation_loss": self.elevation_loss,
            "max_elevation": self.max_elevation,
            "min_elevation": self.min_elevation,
            "type": self.act_type,
            "date": self.date,
            "duration": self.duration
        }

    def __lt__(self, other):
        return self.date < other.date

        
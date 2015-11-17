# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 21:54:27 2015

@author: bhayek
"""

import datetime

import datafile

THRESHOLD = 1
HEADER = ('start', 'stop', 'title', 'seconds')


class logger:
    def __init__(self, log_file):
        self.old_value = ""
        self.log_file = log_file
        self.old_time = self._get_time()
        self.datafile = datafile.datafile(log_file, HEADER)

    def _get_time(self):
        return datetime.datetime.now().replace(microsecond=0)

    def _log_entry(self, values):
        self.datafile.write_csv(values)

    def _close_last(self, old_value, old_time, time_now):
        elapsed = time_now - old_time
        if elapsed > datetime.timedelta(seconds=THRESHOLD):
            self._log_entry([old_time, time_now, old_value, elapsed.seconds])

    def set_value(self, value):
        if value != self.old_value:
            time_now = self._get_time()
            self._close_last(self.old_value, self.old_time, time_now)
            self.old_value = value
            self.old_time = time_now

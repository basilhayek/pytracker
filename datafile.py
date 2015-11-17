# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 15:52:34 2015

@author: bhayek
"""

import csv
import os


class datafile:
    def __init__(self, filename, header):
        self.filename = filename
        self.header = header

    def write_csv(self, values):
        csv_exists = self.file_exists()

        with open(self.filename, 'ab') as f:
            writer = csv.writer(f)
            if not csv_exists:
                writer.writerow(self.header)
            writer.writerow(values)
            f.close()

    def get_filepath(self):
        return self.filename

    def file_exists(self):
        return os.path.isfile(self.filename)

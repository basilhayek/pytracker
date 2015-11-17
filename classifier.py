# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 09:33:00 2015

@author: bhayek
"""

from textblob.classifiers import NaiveBayesClassifier
from textblob.classifiers import DecisionTreeClassifier
import pandas as pd
import numpy as np
import datafile
import analysis
import datetime

MASTER_FILE = 'master.csv'
MASTER_HEADER = ('raw', 'clean', 'class', 'added', 'used')
MASTER_DTYPE = ('string', 'string', 'string', 'datetime64', 'int')


class classifier:
    def __init__(self, train_file):
        self.train_file = train_file
        self.clb = None
        self.master = datafile.datafile(MASTER_FILE, MASTER_HEADER)

    def _load_log(self, log_file):
        df_csv = pd.read_csv(log_file)
        df_csv['start'] = pd.to_datetime(df_csv['start'])
        df_csv['stop'] = pd.to_datetime(df_csv['stop'])
        df_csv['title'].fillna('(unknown)', inplace=True)

        return df_csv

    def run_classifier(self, log_file):
        if self.clb is None:
            with open(self.train_file) as fp_train:
                self.clb = NaiveBayesClassifier(fp_train, format='csv')
        with open(log_file) as fp_test:
            accuracy = self.clb.accuracy(fp_test, format='csv')

    #
    def tag_with_string_ids(self, log_file):

        df = self._load_log(log_file)

        # TODO: Consider how certain items could "fill" time (e.g., a web
        # meeting that fills the 30 minute slot for which it is found)

        # Group the same titles, since we will need to treat these the same
        df_group = df[['title', 'seconds']].groupby(['title']).agg('sum')
        df_group = df_group.reset_index()

        # TODO: Should Pareto happen after window name cleansing?

        # Get the set of values that we need to classify
        df_pareto = analysis.get_pareto(df_group, 'seconds')

        print df_pareto

        # Create the list of new entries to merge
        df_new = df_pareto['title'].reset_index()
        df_new.rename(columns={'title': 'raw'}, inplace='True')

        # TODO: Cleaned versions should exclude version numbers (e.g., v4)
        # and dates (20150901, 2015-09-01)

        # Branch logic based on whether the master file exists
        if self.master.file_exists():
            # Load the existing master
            df_master = pd.read_csv(self.master.get_filepath())

            # Only keep the items with a null class (unclassified)
            df_new = df_new.merge(df_master, how='left', on='raw')
            df_new = df_new[df_new['class'].isnull()]

            # TODO: Attempt to classify based on the master

        else:
            col_types = zip(MASTER_HEADER, MASTER_DTYPE)
            df_master = pd.DataFrame(np.zeros(0, dtype=col_types))

        # Set the attributes for the items that will join the master
        df_new['class'] = "(pending)"
        df_new['clean'] = df_new['raw']
        df_new['added'] = datetime.datetime.now().replace(microsecond=0)
        df_new['used'] = 1  # By default set this to 1

        df_master = df_master.append(df_new[['raw', 'clean', 'class', 'added',
                                             'used']], ignore_index=True)

        # TODO: Get feedback from user as to classes

        # TODO: Apply classification to the df_group items

        # Add rows to the master--this should have the newly classified rows
 #       df_master = df_master.append(df_new[['raw', 'clean', 'class', 'added',
 #                                            'used']], ignore_index=True)

        # Reset the order of the index
        df_master = df_master.reindex_axis(MASTER_HEADER, axis=1)
        df_master.to_csv(self.master.get_filepath())



    def build_train(self, log_file):
        df = self._load_log(log_file)

        print df.head()

        # Grab top X apps to use to create training list
        # Run classifier... prompt user for validation
        # Clasifer will prompt as long as more than 20% is unclassified
        # Other 10% will be assigned according to other 80%


if __name__ == "__main__":

    tl = classifier('app_use_train.csv')
    tl.tag_with_string_ids('app_use_master.csv')

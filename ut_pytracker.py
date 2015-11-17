# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 09:28:55 2015

@author: bhayek
"""


import pytracker
import unittest


class TestTskript(unittest.TestCase):

    def setUp(self):
        return


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTskript)
    unittest.TextTestRunner(verbosity=2).run(suite)

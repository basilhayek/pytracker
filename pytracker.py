# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 09:28:45 2015

@author: bhayek
"""

import win32gui
import datetime
import logger
import time  # For sleep loop
# Run every x minutes (Likely via script...)
# Log time, open window, classification
# At end of day, generate report, show classification, prompt for changes

# Need
# - Update Handler (use inputs from user to update daily TT sheet)
#   - Update Handler should allow for "Prompt" for when there is not enough
#     information to automatically classify
# - Daily Handler (maintain raw filename, optimized filename, classification,
#   timestamp)
# - TT Generator (logic to calculate hours)
# - TT Display (display daily report for user to review)
#   - HTTP Handler (start HTTP server to display report)
# - Classification Handler (randomly select X lines to try to find better
#   classifier)

INTERVAL = 1
LOGFILE = 'app_use.csv'
next_run = datetime.datetime.now()


def get_foreground_window_title():
    hwnd_foreground = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd_foreground)
    return window_title


def interval_hit():
    global next_run
    if datetime.datetime.now() > next_run:
        next_run = next_run + datetime.timedelta(seconds=INTERVAL)
        return True
    return False


def run():
    pylog = logger.logger(LOGFILE)

    while True:
        if interval_hit():
            pylog.set_value(get_foreground_window_title())
        time.sleep(0.2)

# ** MAIN LOOP **
# Sleep and check if interval for checking time has been hit.
# If so, call the tracking logic

if __name__ == "__main__":
    run()

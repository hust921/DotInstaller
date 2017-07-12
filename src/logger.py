#!/usr/bin/python
'''
Simple logger for writing information to a single file.
'''
import datetime
from enum import Enum

class __Loglevel(Enum):
   CRIT = 1
   WARN = 2
   INFO = 3
   DEBUG = 4

   def __str__(self):
       return self.name

CRIT = __Loglevel.CRIT
WARN = __Loglevel.WARN
INFO = __Loglevel.INFO
DEBUG = __Loglevel.DEBUG


class Logger:
    '''Simple, single file logger.'''

    def __init__(self, filename, loglevel=DEBUG):
        self.logfile = filename
        self.loglevel = loglevel

        with open(filename, 'a+') as lfile:
            timestamp = datetime.datetime.now()
            lfile.write("{0} Started: [{1}] {2}\n".format("-"*30, timestamp, "-"*30))

    def log(self, loglevel, msg):
        if loglevel.value <= self.loglevel.value:
            with open(self.logfile, 'a+') as lfile:
                timestamp = datetime.datetime.now()
                lfile.write("[{0}][{1}]: {2}\n".format(loglevel, timestamp, msg))


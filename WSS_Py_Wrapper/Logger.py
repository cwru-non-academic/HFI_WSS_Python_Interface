#!/usr/bin/env python3
   
import configs.Loc as Loc
from datetime import datetime

#take a time reading and name the log file, then open
now = datetime.strftime(datetime.now(), '%Y%m%d%H%M')
logName = Loc.logPath + "/log_" + now + ".txt"

class logFile:
    
    def __init__(self):
        logger = open(logName, "a")
        self.name = logName
        logger.write("begin log_" + now + " at " +  datetime.strftime(datetime.now(), '%H:%M:%S') + "\n")
        logger.close 

    def entry(self, message):
        logger = open(logName, "a")
        logger.write(datetime.strftime(datetime.now(), '%H:%M:%S\t') + message + "\n")
        logger.close

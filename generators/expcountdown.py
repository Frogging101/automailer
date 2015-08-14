from __future__ import division

import os,sys
sys.path.append(os.path.abspath(os.path.dirname(__file__))+"/..")

from taskfs import writeTask
from mailtask import MailTask
from taskgen import TaskGenerator
import taskgen

import time,datetime
import math

class ExpCountdownGenerator(TaskGenerator):
    def __init__(self):
        super(ExpCountdownGenerator, self).__init__()
        self.name = "ExpCountdown"
        self.otherData['Event-Name'] = (str,)
        self.otherData['Event-Date'] = (taskgen.parseDate,)
        self.otherData['Exponent'] = (None,)

        self.internalData["minExponent"] = (int,-5)
        self.internalData["maxExponent"] = (int,8)

        self.sender = "T-Minus <tminus@fastquake.com>"

        self.maxExponent = 8

def secondsToStr(secs):
    out = ''
    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    secs = abs(secs)

    if secs == 90:
        return "90 seconds"
    if secs == 5400:
        return "90 minutes"
    if secs >= 86400:
        days = int(secs/86400)
        out += str(days)
        if days == 1:
            out += " day"
        else:
            out += " days"
        secs -= days*86400
    if secs >= 3600:
        if days > 0:
            out += ', '
        hours = int(secs/3600)
        out += str(hours)
        if hours == 1:
            out += " hour"
        else:
            out += " hours"
        secs -= hours*3600
    if secs >= 60:
        if hours > 0 or days > 0:
            out += ", "
        minutes = int(secs/60)
        out += str(minutes)
        if minutes == 1:
            out += " minute"
        else:
            out += " minutes"
        secs -= minutes*60
    if secs > 0:
        if days > 0 or hours > 0 or minutes > 0:
            out += ", "
        out += str(secs)
        if secs == 1:
            out += " second"
        else:
            out += " seconds"
    return out

#print secondsToStr(int(sys.argv[1]))
#exit(0)

gen = ExpCountdownGenerator()
gen.initFromArgv(sys.argv)

eventDate = gen.otherData['Event-Date']
eventName = gen.otherData["Event-Name"]
minExp = gen.internalData["minExponent"]
maxExp = gen.internalData["maxExponent"]
eventTS = int(time.mktime(eventDate.utctimetuple()))

relativeTimestamps = [int(-((2**x)*86400)) for x in range(minExp,maxExp+1)]
exponents = range(minExp,maxExp+1)

for i,ts in enumerate(relativeTimestamps):
    scheduledTime = eventTS+ts
    if scheduledTime < time.time():
        continue
    remaining = secondsToStr(ts)
    s = remaining+' '
    if remaining[-1:] == 's':
        s += "remain"
    else:
        s += "remains"
    msg = s
    subject = eventName+' - '+s
    gen.otherData["Exponent"] = exponents[i]
    gen.writeMailTask(subject,msg,scheduledTime)


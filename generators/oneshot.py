import os,sys
sys.path.append(os.path.abspath(os.path.dirname(__file__))+"/..")

from taskfs import writeTask
from mailtask import MailTask
from taskgen import TaskGenerator
import taskgen

import time,datetime

class OneShotGenerator(TaskGenerator):
    def __init__(self):
        super(OneShotGenerator, self).__init__()
        self.name = "OneShot"
        self.otherData['Send-At'] = (taskgen.parseDate,)

        self.internalData['Message'] = (str,"Initiator did not specify a message.")
        self.internalData['Subject'] = (str,'')

        self.sender = "FastQuake Automailer <automailer@fastquake.com>"

gen = OneShotGenerator()
gen.initFromArgv(sys.argv)

scheduledTime = int(time.mktime(gen.otherData['Send-At'].utctimetuple()))
msg = gen.internalData['Message']
subject = gen.internalData['Subject']

if not subject:
    subject = "Scheduled message from "+gen.initiator

gen.writeMailTask(subject,msg,scheduledTime)

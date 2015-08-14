import os,sys
sys.path.append(os.path.abspath(os.path.dirname(__file__))+"/..")

from taskfs import writeTask
from mailtask import MailTask
import datetime
import collections
import argparse
import taskfs

try:
    import dateutil.parser
except ImportError:
    pass
    

class TaskGenerator(object):
    def __init__(self):
        self.name = 'DefaultGen'
        self.initiator = None
        self.gentime = None
        self.otherData = collections.OrderedDict()
        self.internalData = {}
    
        self.sender = None # Format: "FastQuake AutoMailer <automailer@fastquake.com>"
        self.recipients = None # ["John Doe <jdoe@fastquake.com>", "Jane Doe <jadoe@fastquake.com>"]
        self.bcc = []
        self.replyto = ""

    def body(self, msg):
        bodystr = ''
        bodystr += "Initiated-By: "+self.initiator+'\n'
        bodystr += "Generator: "+self.name+'\n'
        #bodystr += "Generation-Date: "+self.gentime.isoformat()+'\n'
        if self.otherData:
            bodystr += '\n'

        print dict(self.otherData)
        for k,v in self.otherData.items():
            try:
                bodystr += k+': '+str(v)+'\n'
            except:
                bodystr += k+': null\n'

        bodystr += '\n'
        bodystr += '-----\n'
        bodystr += msg
        bodystr += '\n-----' 
        return bodystr

    def toMailTask(self,subject,msg,scheduledTime):
        mt = MailTask(self.sender,self.recipients,subject,self.body,scheduledTime,
                    bcc=self.bcc,replyto=self.replyto)
        mt.scheduledTime = int(scheduledTime)
        mt.body = self.body(msg)
        mt.subject = subject
        mt.sender = self.sender
        mt.recipients = self.recipients
        mt.bcc = self.bcc

        return mt

    def writeMailTask(self,subject,msg,scheduledTime):
        mt = self.toMailTask(subject,msg,scheduledTime)
        taskfs.writeTask(mt)

    def initFromArgv(self,argv):
        aparser = argparse.ArgumentParser()
        combinedData = self.otherData.copy()
        combinedData.update(self.internalData)
        for k,v in combinedData.items():
            if v[0] is not None:
                if len(v) == 1:
                    aparser.add_argument(k.lower(),type=v[0])
                else:
                    aparser.add_argument('--'+k.lower(),type=v[0],default=v[1])

        if not self.initiator:
            aparser.add_argument("-f", "--from", dest='initiator', default="Unknown")
        if not self.sender:
            aparser.add_argument("sender") #TODO: Validate email
        if not self.recipients:
            aparser.add_argument("-t", "--to",action='append', dest='recipients', required=True)
        if not self.bcc:
            aparser.add_argument("-b", "--to-bcc", action='append', dest='bcc')
        if not self.replyto:
            aparser.add_argument("-r", "--reply-to", dest='replyto')

        args = aparser.parse_args(argv[1:])

        if not self.initiator:
            self.initiator = args.initiator
        if not self.sender:
            self.sender = args.sender
        if not self.recipients:
            self.recipients = args.recipients
        if not self.bcc:
            self.bcc = args.bcc
        if not self.replyto:
            self.replyto = args.replyto
        
        for k,v in self.otherData.items():
            if v[0] is not None:
                self.otherData[k] = getattr(args,k.lower())
        for k,v in self.internalData.items():
            if v[0] is not None:
                self.internalData[k] = getattr(args,k.lower())

def parseDate(dateStr):
    if 'dateutil.parser' in sys.modules:
        dt = dateutil.parser.parse(dateStr, fuzzy=True)
    else:
        dt = datetime.datetime(2017,01,01) #TODO: actually parse a date
    return dt

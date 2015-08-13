import os
import json
from mailtask import MailTask
import hashlib

TASKSDIR = os.path.dirname(os.path.abspath(__file__))+"/tasks/"

# Parses a task object output as a JSON dict
def parseTask(taskjson):
    mtd = json.loads(taskjson)
    sender = str(mtd["sender"])
    replyto = str(mtd["replyto"])
    if mtd["recipients"]:
        recipients = [str(r) for r in mtd["recipients"]]
    else:
        recipients = []
    if mtd["bcc"]:
        bcc = [str(r) for r in mtd["bcc"]]
    else:
        bcc = []
    subject = str(mtd["subject"])
    body = str(mtd["body"])
    scheduledTime = int(mtd["scheduledTime"])
    mt = MailTask(sender,recipients,subject,body,scheduledTime,bcc=bcc,replyto=replyto)
    return mt

def getTasks():
    tasks = set()
    dirlist = os.listdir(TASKSDIR)
    for fn in dirlist:
        path = TASKSDIR+fn
        f = open(path,'r')
        tasks.add(parseTask(f.read()))
        f.close()
    return tasks

def writeTask(task):
    out = json.dumps(task.__dict__)
    dhash = md5Task(task)
    f = open(TASKSDIR+str(task.scheduledTime)+'-'+dhash,'w+')
    f.write(out)
    f.close()

def deleteTask(task):
    try:
        os.remove(TASKSDIR+str(task.scheduledTime)+'-'+md5Task(task))
    except OSError:
        print "Error removing "+str(task.scheduledTime)+"-"+md5Task(task)

def md5Task(task):
    lists = list(task.recipients)
    if task.bcc:
        lists.extend(task.bcc)
    instr = str(task.sender)+str(task.replyto)+\
            reduce(lambda x, y: str(x)+str(y), lists)+\
            str(task.subject)+str(task.body)+str(task.scheduledTime)
    #print "md5ing "+instr
    return hashlib.md5(instr).hexdigest()[:8]

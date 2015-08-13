from intervalexec import IntervalExec
from queue import MailQueue
import taskfs
from taskfs import getTasks
from mailer import Mailer
import time
import copy

def syncQueueToFS(queue):
    print "Syncing queue"
    tasks = getTasks()
    queue.sync(tasks)

def queueConsumer(queue,mlr):
    upcoming = queue.getUpcoming()
    if not upcoming:
        return
    target = list(upcoming)[0].scheduledTime
    curTime = int(time.time())
    if curTime >= target:
        for mtask in upcoming:
            printTS = time.strftime("[%H:%M:%S]")
            late = curTime-target
            print printTS+" Sending mail with subject \""+mtask.subject+"\", "+str(late)+" seconds after target"

            ret = mlr.send(mtask.sender, mtask.replyto, mtask.recipients, mtask.bcc, mtask.subject, mtask.body)
            print ret
            if ret != 0:
                postponed = copy.copy(mtask)
                postponed.scheduledTime += 300
                print "Send failed, delaying 5 minutes"
                taskfs.writeTask(postponed)
            queue.delete(mtask)
            taskfs.deleteTask(mtask)
    pass

myQueue = MailQueue()
mlr = Mailer()
syncIE = IntervalExec(syncQueueToFS, 60, myQueue)
consumerIE = IntervalExec(queueConsumer, 1, (myQueue,mlr))

syncIE.go()
consumerIE.go()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print "Interrupted! Waiting for threads to finish..."
        syncIE.stop()
        consumerIE.stop()
        print "Exiting..."
        exit(0)

import threading
import time

class MailQueue:
    def __init__(self):
        self.tasks = set()  # Set of MailTasks
        self.lock = threading.RLock() # Thread lock
        self.upcoming = set() # Set of next upcoming task(s)

    def add(self,task):
        with self.lock:
            if task not in self.tasks:
                print "Adding task "+str(task)
            self.tasks.add(task)
            if self.upcoming:
                a = list(self.upcoming)[0]
                if task.scheduledTime < a.scheduledTime:
                    self.upcoming = set()
                    self.upcoming.add(task)
                elif task.scheduledTime == a.scheduledTime:
                    self.upcoming.add(task)
            else:
                self.upcoming.add(task)

    def delete(self,task):
        with self.lock:
            if task in self.tasks:
                print "Removing task "+str(task)
                self.tasks.remove(task)
            else:
                print "Attempted to remove nonexistent task "+str(task)+'!'
            if task in self.upcoming:
                self.upcoming.remove(task)

    def sync(self,taskset):
        with self.lock:
            if taskset:
                for thing in taskset:
                    self.add(thing)
                for thing in self.tasks.copy():
                    print str(thing)+" exists internally"
                    if thing not in taskset:
                        print str(thing)+ " does not exist externally, deleting"
                        self.delete(thing)

    def getUpcoming(self):
        with self.lock:
            return set(self.upcoming)

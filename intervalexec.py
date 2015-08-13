import threading
from time import sleep

class IntervalExec:
    def __init__(self, func, interval, args):
        self.run = False    # Runs as long as this is true
        self.func = func    # Function to execute
        self.interval = interval  # Interval in seconds
        self.runlock = threading.RLock()
        self.runthread = None
        self.args = args # Tuple representing arguments
        if not isinstance(self.args, tuple):
            self.args = [self.args]

    def execute(self):
        self.run = True
        with self.runlock:
            run = self.run
        print self.func.__name__+" will now execute every "+str(self.interval)+"s"
        while run:
            self.func(*self.args)
            for sec in range(self.interval):
                sleep(1)
                with self.runlock:
                    run = self.run
                if not run:
                    break
        print self.func.__name__+" executing every "+str(self.interval)+"s Finished"

    def go(self):
        with self.runlock:
            run = self.run
        if not run:
            self.runthread = threading.Thread(target=self.execute)
            self.runthread.start()

    def stop(self):
        with self.runlock:
            self.run = False
            #self.runthread.join()

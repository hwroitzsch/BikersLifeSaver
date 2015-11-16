""" VARIANTE 1 - SIMPEL
import time
from multiprocessing import Process
import datetime

def f(name):
    print (datetime.datetime.now())

if __name__ == '__main__':
    while True:
        #p = Process(target=f, args=('bob',))
        #p.start()
        #p.join()
        f('HA')
        time.sleep(1)
        # time.sleep(0.9957)
"""

""" VARIANTE 2 - PROCESS
from multiprocessing import Process
import time

def doWork():
    while True:
        print "working...."
        time.sleep(10)



if __name__ == "__main__":
    p = Process(target=doWork)
    p.start()

    while True:
        time.sleep(60)
"""

import sched, time
import datetime

scheduler = sched.scheduler(time.time, time.sleep)

def do_something(scheduler):
    print('TIME:', datetime.datetime.now())
    scheduler.enter(1, 1, do_something, (scheduler,))

scheduler.enter(1, 1, do_something, (scheduler,))
scheduler.run()

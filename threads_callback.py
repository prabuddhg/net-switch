# A sample implementation

import threading
import time
from time import sleep

start_time = time.time()
x = {}
x['a'] = {}
x['a']['sample'] = 'apple'
x['b'] = {}
x['b']['sample'] = 'boy'
x['c'] = {}
x['c']['sample'] = 'cat'
y = {}
class MyThread(threading.Thread):
    def __init__(self, callback_function=None, x=None, y=None):
        threading.Thread.__init__(self)
        self.callback = callback_function
        self.x = x
        self.y = y

    def run(self):
            self.callback(x,key,y)


# test

import sys

def count(x):
    print x
    sys.stdout.flush()

def assign_value(x=None,key=None, y=None):
    sleep(1)
    print("--- %s seconds ---" % (time.time() - start_time))
    print x[key]['sample']
    y[key] = x[key]['sample']

for key in x:
    t = MyThread(assign_value,x,y)
    t.start()
    #t.run()
sleep(1.5)
print y
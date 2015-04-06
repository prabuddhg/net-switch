import Queue
import threading
import urllib2
import time
import pprint
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
queue = Queue.Queue()

def assign_value(x=None,key=None):
    sleep(1)
    print("--- %s seconds ---" % (time.time() - start_time))
    return x[key]['sample']

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue=None, x_dict=None, y_dict=None):
        threading.Thread.__init__(self)
        self.queue = queue
        self.x_dict = x_dict
        self.y_dict = y_dict

    def run(self):
        while True:
            key_return = self.queue.get()
            self.y_dict[key_return] = assign_value(self.x_dict,key_return)
            #signals to queue job is done
            self.queue.task_done()

start = time.time()
def main():
    #spawn a pool of threads, and pass them queue instance 
    for key in x:
        t = ThreadUrl(queue, x, y)
        t.setDaemon(True)
        t.start()
        queue.put(key)

queue.join()

main()
sleep(1.5)
print y
from queue import Queue
from threading import Thread
import time
import pprint
import threading

class CommunicatThread(threading.Thread):
    def __init__(self,method=None, que=None):
        threading.Thread.__init__(self)
        self.que = que
        method(que)

def producer(out_q):
    print "\nproducer "
    time.sleep(5)
    out_q.put('hello')

def consumer(in_q):
    print "\nconsumer "
    h = in_q.get()
    print(h + ' world!')
    in_q.task_done()

q = Queue.Queue()
#pprint.pprint(q.__dict__)
t1 = CommunicatThread(producer, q)
#pprint.pprint(q.__dict__)
t2 = CommunicatThread(consumer, q)
#pprint.pprint(q.__dict__)

t1.start()
t2.start()

q.join()
print('q joined!')

'''
thread_1----> queue1
thread_2----> queue1
'''
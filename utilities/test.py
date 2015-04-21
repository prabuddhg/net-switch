from threading import Thread
from time import sleep
import time
start_time = time.time()


threads = [None] * 10
results = [None] * 10
queue = Queue.Queue()
def assign_value(x=None,y=None,key=None):
    sleep(1)
    print("--- %s seconds ---" % (time.time() - start_time))
    return x[key]['sample']

x = {}
x['a'] = {}
x['a']['sample'] = 'apple'
x['b'] = {}
x['b']['sample'] = 'boy'
x['c'] = {}
x['c']['sample'] = 'cat'
print x
y = {}
print("--- %s seconds ---" % (time.time() - start_time))

i=1
for key in x:
    #y[key] = x[key]['sample']
    #thread1 = thread.start_new_thread( assign_value, (x,y,key))
    #thread1.start()
    threads[i] = Thread(target=assign_value, args = (x,y,key))
    #t.daemon = True
    threads[i].start()
    #i=i+1
    #assign_value(x,y,key)
print y


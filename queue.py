import Queue
import pprint
q = Queue.Queue()
print q
for i in range(5):
    q.put(i)

while not q.empty():
    print q.get()
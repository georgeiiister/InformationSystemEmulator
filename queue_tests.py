import queue
import random
import string

queue1 = queue.Queue(size = 10)

for i in range(queue1.size):
    queue1.put(''.join(random.choices(string.ascii_letters,k=10)))

#queue1.dump()

print(queue1.internal_id,queue1.status_lock, sep='\n')

for i in range(len(queue1)):
    print(queue1.get())
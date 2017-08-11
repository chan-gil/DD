from multiprocessing import Process, Queue
import time

sentinel = -1

def creator(data, q):
    print 'Creating data and putting it on the queue'
    for item in data:
        q.put(item)

def my_consumer(q):
    while True:
        data = q.get()
        print 'data found to be processed: {}'.format(data)
        processed = data * 2
        print(processed)
        if data is sentinel:
            q.put(3)
            break

if __name__ == '__main__':
    q = Queue()
    data = [5, 10, 13, -1]

    process_one = Process(target=creator, args=(data, q))
    process_two = Process(target=my_consumer, args=(q,))
    process_one.start()
    process_two.start()
    time.sleep(3)
    print q.get()
    q.close()
    q.join_thread()
    process_one.join()
    process_two.join()

'''
from multiprocessing import Process, Queue, Event
import time

def produce(q, e):
    counter = 1
    while e.is_set():
        item = 'item {0:0>4}'.format(counter)
        print('{} produce: {}'.format(time.time(), item))
        q.put(item)
        
        counter += 1
        time.sleep(0.2)
    print('produce func finish')
        
        
def consume(q, e):
    while e.is_set():
        val = q.get()
        print('{} consume: {}'.format(time.time(), val))
        time.sleep(0.7)
    print('consume func finish')


if __name__ == '__main__':
    q = Queue()
    e = Event()
    e.set()
    p1 = Process(target=produce, args=(q, e))
    p2 = Process(target=consume, args=(q, e))
    
    p1.start()
    p2.start()
    
    print('now main process go to sleep.')
    time.sleep(10)
    print('main process wake up!')
    e.clear()
    print('work flag clear!')
    
    p1.join()
    p2.join()
    
    print('Done!')
'''

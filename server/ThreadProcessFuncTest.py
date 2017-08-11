import threading, time, GuiAR
from multiprocessing import Process, Queue, Lock, Event
from Tkinter import *

class Functest(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        while True:
            print self.func()
            return
        

    def func(self):
        a = 0
        for i in range(self.num):
            a = a + i
        return a

def cout(lock, string):
    lock.acquire()
    try:
        print string
    finally:
        lock.release()
            
def func(lock, queue):
    i = 0
    while queue.empty():
        print i
        i = i + 1
        time.sleep(1)


q = Queue()

if __name__ == '__main__':
    lock = Lock()
    fun = Functest(10)
    gui = GuiAR.GuiAR(q)
    process_one = Process(target=gui.start, args=())
    process_two = Process(target=func, args=(lock, q))
    process_three = Process(target=func, args=(lock, q))

    process_one.start()
    process_two.start()
    process_three.start()    
    fun.start()
    
    fun.join()
    process_two.join()
    process_three.join()
    process_one.join()


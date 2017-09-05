import threading, time
from multiprocessing import Process, Queue, Lock, Event
from Tkinter import *
import Main

class Functest(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        i=0
        while True:
            print i
            i = i+1

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
    #gui = GuiAR.GuiAR(q)
    #process_one = Process(target=gui.start, args=())
    process_two = Process(target=func, args=(lock, q))
    process_three = Process(target=Main.main, args=())

    #process_one.start()
    process_two.start()
    process_three.start()    
    fun.start()
    
    fun.join()
    process_two.join()
    process_three.join()
    #process_one.join()


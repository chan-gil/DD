from multiprocessing import Process, Queue, Lock, Event
#cd Desktop\gradu\server
#python testserver.py
import ServerAR, GuiAR
import sys
import time

def cout(lock, string):
    lock.acquire()
    try:
        print string
    finally:
        lock.release()

def control(cmdQueue, lock, flag):
    cout(lock, "control process started")
    time.sleep(20)
    cmdQueue.put('q')
    flag.set()
    cout(lock, "control process terminated")

def consumer(dataQueue, lock, conQueue):
    cout(lock, "consumer process started")
    while conQueue.empty():
        if not dataQueue.empty():
            cout(lock, dataQueue.get())
        
    print "consumer process terminated"

if __name__ == '__main__':
    dataQueue = Queue()
    cmdQueue = Queue()
    lock = Lock()
    conQueue = Queue()

    server = ServerAR.ServerAR('192.168.123.1', 9003, dataQueue, cmdQueue, lock)
    gui = GuiAR.GuiAR(cmdQueue, conQueue)
    process_one = Process(target=gui.start, args=())
    #process_two = Process(target=control, args=(cmdQueue, lock, flag))
    process_three = Process(target=consumer, args=(dataQueue, lock, conQueue))

    process_one.start()
    #process_two.start()
    process_three.start()
    server.start()

    #dataQueue.close()
    #cmdQueue.close()
    #dataQueue.join_thread()
    #cmdQueue.join_thread()

    server.join()
    process_one.join()
    #process_two.join()
    process_three.join()

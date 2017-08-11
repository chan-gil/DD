from multiprocessing import Process, Queue, Lock, Event
#cd Desktop\gradu\server
#python testserver.py
import ServerAR, GuiAR
import sys
import time
import cv2

def cout(lock, string):
    lock.acquire()
    try:
        print string
    finally:
        lock.release()

def video(videoQueue, lock):
    cam = cv2.VideoCapture('tcp://192.168.1.2:5555')
    while videoQueue.empty():
        # get current frame of video
        running, frame = cam.read()
        if running:
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
        else:
            # error reading frame
            cout(lock,'error reading video feed')
    cam.release()
    cv2.destroyAllWindows()

def consumer(dataQueue, lock, conQueue):
    cout(lock, "consumer process started")
    while conQueue.empty():
        if not dataQueue.empty():
            cout(lock, dataQueue.get())
        
    print "consumer process terminated"

if __name__ == '__main__':
    dataQueue = Queue()
    serverQueue = Queue()
    lock = Lock()
    conQueue = Queue()
    videoQueue = Queue()

    server = ServerAR.ServerAR('192.168.123.1', 9003, dataQueue, serverQueue, lock)
    gui = GuiAR.GuiAR(serverQueue, conQueue, videoQueue)
    process_one = Process(target=gui.start, args=())
    process_two = Process(target=video, args=(videoQueue, lock))
    process_three = Process(target=consumer, args=(dataQueue, lock, conQueue))

    process_one.start()
    process_two.start()
    process_three.start()
    server.start()

    #dataQueue.close()
    #cmdQueue.close()
    #dataQueue.join_thread()
    #cmdQueue.join_thread()

    server.join()
    process_one.join()
    process_two.join()
    process_three.join()

from multiprocessing import Process, Queue, Lock, Event
#cd Desktop\gradu\server
#python testserver.py
import ServerAR, GuiAR
import sys
import time
from datetime import datetime
import cv2

rec = False
running = True
outMode = 'o'

def cout(lock, string):
    lock.acquire()
    try:
        print string
    finally:
        lock.release()

def video(videoQueue, lock):
    cam = cv2.VideoCapture('tcp://192.168.1.2:5555')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    global running, rec, outMode
    while running:
        if not videoQueue.empty():
            outMode = videoQueue.get()
            cout(lock, "data = " + outMode)
        # get current frame of video
        running, frame = cam.read()
        if running:
            if rec:
                out.write(frame)
            if outMode == 'q':
                break
            elif outMode == 'r':
                rec = not rec
                if rec:
                    print "start recording"
                    out = cv2.VideoWriter(initFileName(), fourcc, 25.0, (640,360))
                else:
                    print "stop recording"
                    out.release()
                outMode = preOutMode
            elif outMode =='b' or outMode == 'm' or outMode == 'g':
                img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, frame = cv2.threshold(img_grey,127,255,cv2.THRESH_BINARY)
                if outMode == 'm':
                    frame = cv2.adaptiveThreshold(img_grey,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,2)
                elif outMode == 'g':
                    frame = cv2.adaptiveThreshold(img_grey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)
            preOutMode = outMode
            cv2.imshow('Video', frame)
            cv2.waitKey(1)
        else:
            # error reading frame
            cout(lock,'error reading video feed')
    cam.release()
    cv2.destroyAllWindows()

def initFileName():
    fileName = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + "-" + str(datetime.now().hour) + "-" + str(datetime.now().minute) + "-" + str(datetime.now().second) + ".avi"
    return fileName


def consumer(dataQueue, lock, conQueue):
    cout(lock, "consumer process started")
    while conQueue.empty():
        if not dataQueue.empty():
            dataIn = dataQueue.get()
            cout(lock, dataIn)
            if dataIn == 'b':
                videoQueue.put('b')

        
    print "consumer process terminated"

if __name__ == '__main__':
    dataQueue = Queue()
    serverQueue = Queue()
    lock = Lock()
    conQueue = Queue()
    videoQueue = Queue()

    # server = ServerAR.ServerAR('192.168.123.1', 9003, dataQueue, serverQueue, lock)
    gui = GuiAR.GuiAR(serverQueue, conQueue, videoQueue)
    process_one = Process(target=gui.start, args=())
    process_two = Process(target=video, args=(videoQueue, lock))
    process_three = Process(target=consumer, args=(dataQueue, lock, conQueue))

    process_one.start()
    process_two.start()
    process_three.start()
    # server.start()

    #dataQueue.close()
    #cmdQueue.close()
    #dataQueue.join_thread()
    #cmdQueue.join_thread()

    #server.join()
    process_one.join()
    process_two.join()
    process_three.join()

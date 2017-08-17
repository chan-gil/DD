##############
### IMPORT ###
##############
from multiprocessing import Process, Queue, Lock, Event
#cd Desktop\gradu\server
#python testserver.py
from datetime import datetime
import sys, time
import threading
import cv2
import ServerAR, GuiAR
import ARDroneLib, ARDroneGUI
from ARDroneLog import Log

###############
### GLOBALS ###
###############
last_coord=(None,None)
all_coords = dict()
rec = False
running = True
outMode = 'o'

##################
#   FUNCTIONS    #
##################
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
                    out = cv2.VideoWriter(initFileName(1), fourcc, 25.0, (640,360))
                else:
                    print "stop recording"
                    out.release()
                outMode = preOutMode
            elif outMode == 'p':
                cv2.imwrite(initFileName(0), frame)
                outMode = preOutMode
            if outMode =='b' or outMode == 'm' or outMode == 'g':
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

def initFileName(num):
    if num == 0:
        print 'image save'
        fileName = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + "-" + str(datetime.now().hour) + "-" + str(datetime.now().minute) + "-" + str(datetime.now().second) + ".jpeg"
    elif num == 1:
        print 'video save'
        fileName = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + "-" + str(datetime.now().hour) + "-" + str(datetime.now().minute) + "-" + str(datetime.now().second) + ".avi"
    return fileName


def consumer(dataQueue, lock, conQueue, drone):
    cout(lock, "consumer process started")

    while conQueue.empty():
        if not dataQueue.empty():
            dataIn = dataQueue.get()
            cout(lock, dataIn)
            '''
            if dataIn == '8':
                print "hover"
                drone.hover()
            elif dataIn == '100':
                print "take off"
                drone.takeoff()
            elif dataIn == '101':
                print "land"
                drone.land()
            elif dataIn == '1':
                print "forward"
                drone.forward()
            elif dataIn == '4':
                print "backward"
                drone.backward()
            elif dataIn == '3':
                print "left"
                drone.left()
            elif dataIn == '5':
                print "right"
                drone.right()
            elif dataIn == '0':
                print "left spin"
                drone.rotate_left()
            elif dataIn == '2':
                print "right spin"
                drone.rotate_right()
            elif dataIn == '200':
                videoQueue.put('q')
            elif dataIn == '201':
                videoQueue.put('r')
            elif dataIn == '202':
                videoQueue.put('p')
            elif dataIn == '250':
                videoQueue.put('o')
            elif dataIn == '251':
                videoQueue.put('b')
            elif dataIn == '252':
                videoQueue.put('m')
            elif dataIn == '253':
                videoQueue.put('g')'''

    #drone.stop()
    print "consumer process terminated"

if __name__ == '__main__':
    global drone
    '''try :
        drone = ARDroneLib.Drone("192.168.1.2")
    except IOError:
        wait = raw_input("-> Cannot connect to drone !\n-> Press return to quit...")
        sys.exit()'''
    dataQueue = Queue()
    serverQueue = Queue()
    lock = Lock()
    conQueue = Queue()
    videoQueue = Queue()    
    print '''
    outMode = 'q'   // quit
    outMode = 'r'   // recording start/stop
    outMode = 'p'   // save current frame

    outMode = 'o'   // original video
    outMode = 'b'   // binary filter
    outMode = 'm'   // mean filter
    outMode = 'g'   // gaussian filterf
    '''
    drone = None
    server = ServerAR.ServerAR('192.168.123.1', 9000, dataQueue, serverQueue, lock)
    gui = GuiAR.GuiAR(serverQueue, conQueue, videoQueue)
    process_one = Process(target=gui.start, args=())
    #process_two = Process(target=video, args=(videoQueue, lock))
    thread_two = threading.Thread(target=consumer, args=(dataQueue, lock, conQueue, drone))

    process_one.start()
    #process_two.start()
    thread_two.start()
    server.start()

    #dataQueue.close()
    #cmdQueue.close()
    #dataQueue.join_thread()
    #cmdQueue.join_thread()

    server.join()
    process_one.join()
    #process_two.join()
    thread_two.join()

    print "Test done"


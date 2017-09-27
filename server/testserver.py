##############
### IMPORT ###
##############
from multiprocessing import Process, Queue, Lock, Event
#cd Desktop\gradu\server
#python testserver.py
# path : C:\Users\huiba\Downloads\Drone\test\DDL\server
from datetime import datetime
import sys, time
import threading
#import cv2
import ServerAR, GuiAR, videoAR
import ARDroneLib, ARDroneGUI
#from ARDroneLog import Log

###############
### GLOBALS ###
###############

#pos = GPS_Coord()

###############
### CLASSES ###
###############

class GPS_Coord():
    "Very little class to store GPS Coord"
    def setPoint(self, longi=None, lati=None):
        self.lo = longi
        self.la = lati
        print "> Saved navpoint:",(self.lo,self.la)
    def getPoint(self): return (self.lo, self.la)


##################
#   FUNCTIONS    #
##################
def cout(lock, string):
    lock.acquire()
    try:
        print string
    finally:
        lock.release()

def consumer(dataQueue, lock, conQueue, drone):
    cout(lock, "consumer process started")
    speed = 0.1
    while conQueue.empty():
        if not dataQueue.empty():
            dataIn = dataQueue.get()
            cout(lock, dataIn)
            if dataIn == '8':
                drone.hover()
            elif dataIn == '100':
                drone.takeoff()
            elif dataIn == '101':
                drone.land()
            elif dataIn == '1':
                drone.forward(speed)
            elif dataIn == '4':
                drone.backward(speed * 4)
            elif dataIn == '3':
                drone.left(speed * 2)
            elif dataIn == '5':
                drone.right(speed * 2)
            elif dataIn == '0':
                drone.rotate_left(speed * 4)
            elif dataIn == '2':
                drone.rotate_right(speed * 2)
            elif dataIn == '6':
                drone.up(speed * 2)
            elif dataIn == '7':
                drone.down(speed * 2)
            elif dataIn == 'g':
                drone.goto("gps", pos.getPoint()[0], pos.getPoint()[1], 2, continuous=True)
            # video Queue
            elif dataIn == '200':
                videoQueue.put('q')
            elif dataIn == '201':
                videoQueue.put('r')
            elif dataIn == '202':
                 videoQueue.put('p')
    drone.land()
    drone.stop()
    print "consumer process terminated"

def location(locationQueue, lock):

    template = cv2.imread('drone.PNG')
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    cam = cv2.VideoCapture(0)
    running = True
    while running:
        # get current frame of video
        if not locationQueue.empty():
            break
        
        running, frame = cam.read()
        if running:
            # Convert to grayscale
            imageGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
            # Find template
            result = cv2.matchTemplate(imageGray,templateGray, cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            top_left = max_loc
            h,w = templateGray.shape
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(frame,top_left, bottom_right,(0,0,255),4)

            cv2.imshow('frame', frame)
            cv2.waitKey(1)
        else:
            # error reading frame
            cout(lock, 'error reading video feed')
            
    cam.release()
    cv2.destroyAllWindows()
        
    

if __name__ == '__main__':
    global drone
    drone = None
    try :
        drone = ARDroneLib.Drone("192.168.1.2")
    except IOError:
        wait = raw_input("-> Cannot connect to drone !\n-> Press return to quit...")
        sys.exit()
    dataQueue = Queue()
    serverQueue = Queue()
    lock = Lock()
    conQueue = Queue()
    videoQueue = Queue()
    locationQueue = Queue()
    frameQueue = Queue()
    frameFlagQueue = Queue()
    navDataQueue = Queue()
    print '''
    outMode = 'q'   // quit
    outMode = 'r'   // recording start/stop
    outMode = 'p'   // save current frame

    outMode = 'o'   // original video
    outMode = 'b'   // binary filter
    outMode = 'm'   // mean filter
    outMode = 'g'   // gaussian filterf
    '''
    
    #server = ServerAR.ServerAR('192.168.123.1', 9000, dataQueue, serverQueue, frameQueue, frameFlagQueue, lock)
    gui = GuiAR.GuiAR(serverQueue, conQueue, videoQueue, locationQueue, dataQueue)
    video = videoAR.VideoAR(lock, videoQueue, frameQueue, frameFlagQueue, dataQueue, navDataQueue)
    process_one = Process(target=gui.start, args=())
    process_two = Process(target=video.video, args=())
    #process_three = Process(target=location, args=(locationQueue, lock))
    thread_two = threading.Thread(target=consumer, args=(dataQueue, lock, conQueue, drone))

    drone.set_callback(navDataQueue)
    drone.set_config(activate_navdata=True, detect_tag=1, activate_gps=True)

    process_one.start()
    process_two.start()
    #process_three.start()
    thread_two.start()
    #server.start()

    #server.join()
    process_one.join()
    #process_three.join()
    process_two.join()
    thread_two.join()

    print "Test done"


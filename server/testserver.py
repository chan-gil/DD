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
import ServerAR, GuiAR, videoAR, MapAR
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
                drone.left(speed)
            elif dataIn == '5':
                drone.right(speed)
            elif dataIn == '0':
                drone.rotate_left(speed * 5)
            elif dataIn == '2':
                drone.rotate_right(speed * 5)
            elif dataIn == '6':
                drone.up(speed=1)
                drone.up(speed=1)
                drone.up(speed=1)
                drone.up(speed=1)
            elif dataIn == '7':
                drone.down(speed * 2)
            elif dataIn == 'g':
                count = 0
                loc = [None] * 4
                while not count == 4:
                    if not dataQueue.empty():
                        loc[count] = dataQueue.get()
                        count = count + 1
                if not loc[1] == "xx.xxxxxx":
                    cout(lock, "go to")
                    #drone.goto("gps", loc[0], loc[1], 2, continuous=True)
                if loc[3] == "Tracking":
                    cout(lock, "tracking")
                    videoQueue.put('t')
            elif dataIn == 'r':
                drone.reset()
            # video Queue
            elif dataIn == '200':
                videoQueue.put('q')
            elif dataIn == '201':
                videoQueue.put('r')
            elif dataIn == '202':
                videoQueue.put('p')
            elif dataIn == '400':
                videoQueue.put('m')
    drone.land()
    drone.stop()
    cout(lock, "consumer process terminated")
   
def location(locationQueue):
    startX = 37.497492
    startY = 126.955535
    dx = -0.000002
    dy = 0.000101
    for i in range(10):
        locationQueue.put((startX, startY))
        startX = startX + dx
        startY = startY + dy
    locationQueue.put(('q','q'))

    

if __name__ == '__main__':
    global drone
    drone = None
    '''
    try :
        drone = ARDroneLib.Drone("192.168.1.2")
    except IOError:
        wait = raw_input("-> Cannot connect to drone !\n-> Press return to quit...")
        sys.exit()
        '''
    dataQueue = Queue()
    serverQueue = Queue()
    lock = Lock()
    conQueue = Queue()
    videoQueue = Queue()
    locationQueue = Queue()
    frameQueue = Queue()
    frameFlagQueue = Queue()
    navDataQueue = Queue()
    mapQueue = Queue()

    print '''
    outMode = 'q'   // quit
    outMode = 'r'   // recording start/stop
    outMode = 'p'   // save current frame

    outMode = 'o'   // original video
    outMode = 'b'   // binary filter
    outMode = 'm'   // mean filter
    outMode = 'g'   // gaussian filterf
    '''
    
    server = ServerAR.ServerAR('192.168.123.1', 9000, dataQueue, serverQueue, frameQueue, frameFlagQueue, lock, mapQueue)
    gui = GuiAR.GuiAR(serverQueue, conQueue, videoQueue, locationQueue, dataQueue)
    video = videoAR.VideoAR(lock, videoQueue, frameQueue, frameFlagQueue, dataQueue, navDataQueue)
    mapGPS = MapAR.MapAR(locationQueue, mapQueue)

    process_one = Process(target=gui.start, args=())
    process_two = Process(target=video.video, args=())
    #process_three = Process(target=location, args=(locationQueue, lock))
    thread_two = threading.Thread(target=consumer, args=(dataQueue, lock, conQueue, drone))
    process_four = Process(target=mapGPS.mapping, args = ())

    #drone.set_callback(navDataQueue)
    #drone.set_config(activate_navdata=True, detect_tag=1, activate_gps=True)

    process_one.start()
    process_two.start()
    #process_three.start()
    thread_two.start()
    server.start()
    process_four.start()

    server.join()
    process_one.join()
    #process_three.join()
    process_two.join()
    thread_two.join()
    process_four.join()

    print "Test done"


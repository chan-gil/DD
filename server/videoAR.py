from datetime import datetime
import cv2
import ARDroneLib, ARDroneGUI
from ARDroneLog import Log

class VideoAR():
    def __init__(self, lock, videoQueue, frameQueue, frameFlagQueue):
        self.lock = lock
        self.videoQueue = videoQueue
        self.frameQueue = frameQueue
        self.frameFlagQueue = frameFlagQueue 
        self.cam = cv2.VideoCapture('tcp://192.168.1.2:5555')
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.running = True
        self.rec = False
        self.outMode = None
        self.frame = None

    def video(self):
        while self.running:
            if not self.videoQueue.empty():
                self.outMode = self.videoQueue.get()
                cout("data = " + self.outMode)
            # get current frame of video
            self.running, self.frame = self.cam.read()
            if self.running:
                if self.rec:
                    out.write(self.frame)
                if self.outMode == 'q':
                    break
                elif self.outMode == 'r':
                    self.rec = not self.rec
                    if self.rec:
                        self.cout("start recording")
                        out = cv2.VideoWriter(self.initFileName(1), self.fourcc, 25.0, (640,360))
                    else:
                        self.cout("stop recording")
                        out.release()
                    self.outMode = preOutMode
                elif self.outMode == 'p':
                    cv2.imwrite(self.initFileName(0), self.frame)
                    self.outMode = preOutMode                
                if self.outMode =='b' or self.outMode == 'm' or self.outMode == 'g':
                    img_grey = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    ret, frame = cv2.threshold(img_grey,127,255,cv2.THRESH_BINARY)
                    if self.outMode == 'm':
                        self.frame = cv2.adaptiveThreshold(img_grey,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,2)
                    elif self.outMode == 'g':
                        self.frame = cv2.adaptiveThreshold(img_grey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)
                preOutMode = self.outMode
                cv2.imshow('Video', self.frame)
                self.tossFrame()
                cv2.waitKey(1)
            else:
                # error reading frame
                self.cout('error reading video feed')
        self.cam.release()
        cv2.destroyAllWindows()

    def tossFrame(self):
        if not self.frameFlagQueue.empty():
            self.frameFlagQueue.get()
            if not self.frame == None:
                self.frameQueue.put(self.frame)
        
    def initFileName(self, num):
        if num == 0:
            self.cout('image save')
            fileName = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + "-" + str(datetime.now().hour) + "-" + str(datetime.now().minute) + "-" + str(datetime.now().second) + ".jpeg"
        elif num == 1:
            self.cout('video save')
            fileName = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + "-" + str(datetime.now().hour) + "-" + str(datetime.now().minute) + "-" + str(datetime.now().second) + ".avi"
        return fileName

    def cout(self, string):
        self.lock.acquire()
        try:
            print string
        finally:
            self.lock.release()

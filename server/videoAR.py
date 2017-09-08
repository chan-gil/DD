from datetime import datetime
import cv2
import numpy as np
import os

import ARDroneLib, ARDroneGUI
from ARDroneLog import Log
from PIL import Image
from io import BytesIO


import DetectChars
import DetectPlates
import PossiblePlate

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = True
###################################################################################################


class VideoAR():
    def __init__(self, lock, videoQueue, frameQueue, frameFlagQueue, dataQueue):
        self.lock = lock
        self.videoQueue = videoQueue
        self.frameQueue = frameQueue
        self.frameFlagQueue = frameFlagQueue 
        self.dataQueue = dataQueue
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.running = True
        self.rec = False
        self.outMode = None
        self.frame = None
        self.windowX1 = 640 * 4 / 10
        self.windowX2 = 640 * 6 / 10
        self.windowY1 = 360 * 4 / 10
        self.windowY2 = 360 * 6 / 10
        self.hoverCount = 0
        self.baseS = 4500
        self.baseR = 7


    def video(self):
        cam = cv2.VideoCapture('tcp://192.168.1.2:5555')
        self.lock.acquire()
        try:
            blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training
            if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
                print "\nerror: KNN traning was not successful\n"               # show error message
        finally:
            self.lock.release()
        while self.running:
            if not self.videoQueue.empty():
                self.outMode = self.videoQueue.get()
                self.cout("data = " + self.outMode)
            # get current frame of video
            self.running, self.frame = cam.read()
            #self.cout(str(self.frame.shape))
            if self.running:
                ######## recording ########
                if self.rec:
                    out.write(self.frame)
                # quit
                if self.outMode == 'q': 
                    break
                # change recording flag
                elif self.outMode == 'r':
                    self.rec = not self.rec
                    if self.rec:
                        self.cout("start recording")
                        out = cv2.VideoWriter(self.initFileName(1), self.fourcc, 25.0, (640,360))
                    else:
                        self.cout("stop recording")
                        out.release()
                    self.outMode = preOutMode
                # take picture
                elif self.outMode == 'p':
                    cv2.imwrite(self.initFileName(0), self.frame)
                    self.outMode = preOutMode                
                # apply filter 
                if self.outMode =='b' or self.outMode == 'm' or self.outMode == 'g':
                    img_grey = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    ret, self.frame = cv2.threshold(img_grey,127,255,cv2.THRESH_BINARY)
                    if self.outMode == 'm':
                        self.frame = cv2.adaptiveThreshold(img_grey,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,2)
                    elif self.outMode == 'g':
                        self.frame = cv2.adaptiveThreshold(img_grey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)
                # tracking
                elif self.outMode == 't':
                    # self.lock.acquire()
                    # try:
                    #     #self.licenseTracking()
                    # finally:
                    #     self.lock.release()
                    self.licenseTracking()
                preOutMode = self.outMode


                cv2.imshow('Video', self.frame)
                self.tossFrame()
                cv2.waitKey(1)
            else:
                # error reading frame
                self.cout('error reading video feed')
        cam.release()    
        cv2.destroyAllWindows()


    def licenseTracking(self):

        listOfPossiblePlates = DetectPlates.detectPlatesInScene(self.frame)           # detect plates
        #print listOfPossiblePlates
        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

        targetPlate = -1
        # targetNum = raw_input("input number : ")
        targetNum = 3108
        targetX = 0
        targetY = 0
        

        if len(listOfPossiblePlates) == 0:                          # if no plates were found
            # print "\nno license plates were detected\n"             # inform user no plates were found
            pass
        else:                                                       # else
                    # if we get in here list of possible plates has at leat one plate

                    # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
            #listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                    # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
            numOfPlates = len(listOfPossiblePlates)

            #cv2.imshow("imgPlate", licPlate.imgPlate)           # show crop of plate and threshold of plate
            while numOfPlates > 0:
                numOfPlates = numOfPlates - 1
                try:
                    num = int(listOfPossiblePlates[numOfPlates].strChars) % 10000
                    if num == int(targetNum):
                        targetPlate = numOfPlates
                        #print "target detected\n\n"
                except:
                    pass
                #cv2.imshow(str(numOfPlates), listOfPossiblePlates[numOfPlates].imgThresh)

            #if len(listOfPossiblePlates[0].strChars) == 0:      # if no chars were found in the plate
            #     print "\nno characters were detected\n\n"       # show message
            #     return                                          # and exit program
            # end if

            if targetPlate != -1:
                self.drawRedRectangleAroundPlate(self.frame, listOfPossiblePlates[targetPlate])             # draw red rectangle around plate
                # print "\nlicense plate read from image = " + listOfPossiblePlates[targetPlate].strChars + "\n"       # write license plate text to std out
                #writeLicensePlateCharsOnImage(imgOriginalScene, listOfPossiblePlates[targetPlate])           # write license plate text on the image
                #self.coordinatesQueue.put((listOfPossiblePlates[targetPlate].rrLocationOfPlateInScene[0][0],listOfPossiblePlates[targetPlate].rrLocationOfPlateInScene[0][1]))
                targetX = listOfPossiblePlates[targetPlate].rrLocationOfPlateInScene[0][0]
                targetY = listOfPossiblePlates[targetPlate].rrLocationOfPlateInScene[0][1]
                # print "target x : " + str(targetX)
                # print "target y : " + str(targetY)
        self.boundCheck(targetPlate, targetX, targetY)

    def drawRedRectangleAroundPlate(self, imgOriginalScene, licPlate):
        self.p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect
        cv2.line(imgOriginalScene, tuple(self.p2fRectPoints[0]), tuple(self.p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
        cv2.line(imgOriginalScene, tuple(self.p2fRectPoints[1]), tuple(self.p2fRectPoints[2]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(self.p2fRectPoints[2]), tuple(self.p2fRectPoints[3]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(self.p2fRectPoints[3]), tuple(self.p2fRectPoints[0]), SCALAR_RED, 2)
        cv2.rectangle(imgOriginalScene, (self.windowX1, self.windowY1), (self.windowX2, self.windowY2), SCALAR_GREEN, 2)
        cv2.circle(imgOriginalScene, (int(licPlate.rrLocationOfPlateInScene[0][0]), int(licPlate.rrLocationOfPlateInScene[0][1])), 1, SCALAR_RED, 2)
    
    def boundCheck(self, flag, x, y):
        if flag == -1:
            self.hoverCount = self.hoverCount - 1
            if self.hoverCount <= 0:
                self.dataQueue.put('8')
                self.hoverCount = 0
            return

        self.hoverCount = 3
        '''# move1
        if x < self.windowX1:
            self.dataQueue.put('3') # left
        elif x > self.windowX2:
            self.dataQueue.put('5') # rignt
        # else:
        #     self.dataQueue.put('8')

        if y < self.windowY1:
            self.dataQueue.put('6') # up
        elif y > self.windowY2:
            self.dataQueue.put('7') # down
        # else:
        #     self.dataQueue.put('8')
        '''

        #move2

        # else:
        #     self.dataQueue.put('8')
        
        x1, y1 = self.p2fRectPoints[0] # left top
        x2, y2 = self.p2fRectPoints[2] # right bottom
        a = abs(x1 - x2) # x length
        b = abs(y1 - y2) # y length
        r = b / a # ratio

        s = a * b # box size

        if s < self.baseS:
            self.dataQueue.put('1') # forward
        elif s > self.baseS:
            self.dataQueue.put('7') # backward

        if not (r < self.baseR * 0.9 or r > self.baseR * 1.1):
            return

        if  s > self.baseS * 0.9 and s < self.baseS * 1.1:
            self.dataQueue.put('8')
            return
        
        
        if x < self.windowX1:
            self.dataQueue.put('0') # left spin
        elif x > self.windowX2:
            self.dataQueue.put('2') # rignt spin
        # else:
        #     self.dataQueue.put('8')

    # end function

    def tossFrame(self):
        if not self.frameFlagQueue.empty():
            self.frameFlagQueue.get()
            #self.cout("videoF")
            try:
                img = Image.fromarray(self.frame)
                with BytesIO() as f:
                    img.save(f, format='JPEG')
                    self.frameQueue.put(f.getvalue())
                    
                #img.show()
            except Exception, e :
                self.cout(e)
                self.cout("toss error : 1")
        
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

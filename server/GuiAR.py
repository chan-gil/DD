from Tkinter import *
import time
from multiprocessing import Process, Queue, Lock, Event

class GuiAR():
    "Create a simple window to control the drone"
    def __init__(self, serverQueue, conQueue, videoQueue, locationQueue, dataQueue):
        self.FPS = 5
        self.text = None
        self.text_label = None
        self.fen = None
        self.running = False
        self.last_key = None
        self.actions = dict()   # Actions associated to keys
        self.serverQueue = serverQueue
        self.conQueue = conQueue
        self.videoQueue = videoQueue
        self.locationQueue = locationQueue
        self.dataQueue = dataQueue
        # self.to_print = list()
        # self.text = None

    def add_action(self,button_bind,function_call):
        "Add an action when a key is pressed"
        self.actions[button_bind] = function_call
        return True

    def start(self):
        "Activate the window (and keep the thread)"
        self.fen = Tk()
        self.cadre = Frame(self.fen, width=500, height = 200, bg="grey")
        self.text = StringVar() # Text that will be changed
        self.text_label = Label(self.fen,textvariable=self.text, fg = "black")
        self.text_label.pack()
        self.fen.bind("<KeyPress>",self._key_pressed)
        self.fen.bind("<KeyRelease>",self._key_released)
        self.cadre.pack()
        self.fen.protocol("WM_DELETE_WINDOW", self.stop) # Called when the window is closed


        self.add_action('q', self.close)

        self.add_action('h', self.control_hover)
        self.add_action('u', self.control_up)
        self.add_action('j', self.control_down)
        self.add_action('e', self.control_forward)
        self.add_action('d', self.control_backward)
        self.add_action('s', self.control_left)
        self.add_action('f', self.control_right)
        self.add_action('w', self.control_leftTurn)
        self.add_action('r', self.control_rightTurn)

        buttonRec = Button(self.fen, text = 'Record', command = self.rec)
        buttonRec.pack()
        buttonPic = Button(self.fen, text = 'Take Picture', command = self.pic)
        buttonPic.pack()
        # buttonBin = Button(self.fen, text = 'Binary', command = self.bin)
        # buttonBin.pack()
        # buttonMen = Button(self.fen, text = 'Mean', command = self.men)
        # buttonMen.pack()
        # buttonGau = Button(self.fen, text = 'Gaussian', command = self.gau)
        # buttonGau.pack()
        buttonOri = Button(self.fen, text = 'Original', command = self.ori)
        buttonOri.pack()
        buttonTrack = Button(self.fen, text = 'Tracking', command = self.tracking)
        buttonTrack.pack()
        buttonTakeoff = Button(self.fen, text = 'Takeoff', command = self.takeoff)
        buttonTakeoff.pack()
        buttonLand = Button(self.fen, text = 'Land', command = self.land)
        buttonLand.pack()
        buttonHover = Button(self.fen, text = 'Hover', command = self.hover)
        buttonHover.pack()
        buttonGPS = Button(self.fen, text = 'GPS', command = self.gps)
        buttonGPS.pack()
        buttonR = Button(self.fen, text = 'R', command = self.btnR)
        buttonR.pack()
        buttonReset = Button(self.fen, text = 'Reset', command = self.reset)
        buttonReset.pack()

        #self.fen.mainloop()
        self.running = True
        while self.running:
            self.fen.update()
            time.sleep(1.0/self.FPS) # Adjust FPS

    def reset(self):
        self.dataQueue.put('r')
    def btnR(self):
        self.serverQueue.put('r')
    def rec(self):
        self.videoQueue.put('r')
    def bin(self):
        self.videoQueue.put('b')
    def men(self):
        self.videoQueue.put('m')
    def gau(self):
        self.videoQueue.put('g')
    def ori(self):
        self.videoQueue.put('o')
    def pic(self):
        self.videoQueue.put('p')
    def tracking(self):
        self.videoQueue.put('t')
        self.videoQueue.put('3108')
    def takeoff(self):
        self.dataQueue.put('100')
    def land(self):
        self.dataQueue.put('101')
    def hover(self):
        self.dataQueue.put('8')
    def gps(self):
        self.dataQueue.put('c')

    def close(self):
        self.serverQueue.put('q')
        self.serverQueue.put('q')
        self.conQueue.put('q')
        self.videoQueue.put('q')
        self.locationQueue.put('q')
        self.stop()
        return True

    def control_up(self):
        self.dataQueue.put('6')
    def control_down(self):
        self.dataQueue.put('7')
    def control_forward(self):
        self.dataQueue.put('1')
    def control_backward(self):
        self.dataQueue.put('4')
    def control_right(self):
        self.dataQueue.put('5')
    def control_left(self):
        self.dataQueue.put('3')
    def control_rightTurn(self):
        self.dataQueue.put('2')
    def control_leftTurn(self):
        self.dataQueue.put('0')
    def control_hover(self):
        self.dataQueue.put('8')
            
    def stop(self):
        "Stop the window"
        self.serverQueue.put('q')
        self.serverQueue.put('q')
        self.conQueue.put('q')
        self.videoQueue.put('q')
        try:    self.fen.destroy()
        except: pass
        try:    self.fen.quit()
        except: pass
        self.running = False
        return True

    # Keys handler
    def _key_pressed(self, action):
        "Function which is called when a key is pressed"
        if self.last_key != action.keysym : # Check if it's new key
            self.last_key = action.keysym
            if action.keysym in self.actions.keys(): # Check if we need to perform action
                self.actions[action.keysym]()
    def _key_released(self,action):
        "Function called when the key is released"
        if self.last_key != None:
            self.last_key = None

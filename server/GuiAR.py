from Tkinter import *
#from tkinter import ttk
import time
from multiprocessing import Process, Queue, Lock, Event

class GuiAR():
    def __init__(self, serverQueue, conQueue, videoQueue):
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
        buttonRed = Button(self.fen, text = 'Red', command = self.red)
        buttonRed.pack()
        
        #self.fen.mainloop()
        self.running = True
        while self.running:
            self.fen.update()
            time.sleep(1.0/self.FPS) # Adjust FPS

    def red(self):
        self.serverQueue.put('r')

    def close(self):
        self.serverQueue.put('q')
        self.conQueue.put('q')
        self.videoQueue.put('q')
        return True

            
    def stop(self):
        "Stop the window"
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

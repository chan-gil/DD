import socket
import threading
from multiprocessing import Queue, Lock
import errno

class ServerAR(threading.Thread):

    # exception handle request
    def __init__(self, host, port, dataQueue, cmdQueue, frameQueue, frameFlagQueue, lock):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.dataQueue = dataQueue
        self.cmdQueue = cmdQueue
        self.frameQueue = frameQueue
        self.frameFlagQueue = frameFlagQueue
        self.lock = lock
        self.cmd = 'N'
        self.isConn = False
        self.conn = None
        self.addr = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(1)
        self.togle = True

        self.f1 = open('drone.jpg','rb')# open file as binary
        self.data1 = self.f1.read()
        self.l1 = len(self.data1)
        self.f2 = open('map (2).jpg','rb')# open file as binary
        self.data2 = self.f2.read()
        self.l2 = len(self.data2)
        self.f1.flush()
        self.f2.flush()
        self.f1.close()
        self.f2.close()
        self.frameFlagQueue.put('n')

    def __del__(self):
        try:
            self.conn.close()
        except :
            pass

    def run(self):
        # server connection
        while 1:
            try:
                if self.cmdCheck():
                    break
                self.cout("connection waiting")
                self.s.settimeout(3)
                self.conn, self.addr = self.s.accept() #accept client
                self.isConn = True
                if self.isConn:
                    self.cout("Connected by ")
                    self.cout(self.addr)
                    #self.s.settimeout(None)
            except socket.timeout:
                self.isConn = False
                self.cout("timeout")
            except Exception, e :
                self.cout(e)
                self.cout("connection error : 2")
                break

        # server run
            while True:
                if not self.isConn:
                    break
                if self.cmdCheck():
                    break                

                try :
                    data = self.conn.recv(1024) #recieve message
                    msg = data.split()
                    self.cout(msg)
                    for i in range(len(msg) / 2):
                        if msg[2 * i] == 'msg':
                            self.dataQueue.put(msg[2 * i + 1])
                            if msg[2 * i + 1] == '200':
                                #print "quit"
                                raise Exception
                except socket.error, e:
                    if e.errno == errno.ECONNRESET:
                        self.isConn = False
                        self.cout(e)
                        self.cout("recv errer : 2")
                    pass
                except Exception, e :
                    self.cout(e)
                    self.cout("recv errer : 1")
                    self.isConn = False
                    #drone.stop()
                    break

                self.frame()

    def frame(self):
        if not self.frameQueue.empty():
            self.lock.acquire()
            try:
                f = self.frameQueue.get()
                self.conn.sendall("msg r " + str(len(f)) + "\n")
                self.conn.sendall(f)
            except Exception, e :
                print e
                print "send errer : 2"
            finally:
                self.lock.release()
                self.frameFlagQueue.put('n')
                
                
    def cout(self, string):
        self.lock.acquire()
        try:
            print string
        finally:
            self.lock.release()

    def cmdCheck(self):
        if not self.cmdQueue.empty():
            self.cmd = self.cmdQueue.get()
            if self.cmd == 'q':
                self.cout("recv ended")
                return True
            if self.isConn and self.cmd == 'r':
                self.lock.acquire()
                try:
                    if self.togle:
                        self.conn.sendall("msg r " + str(self.l1) + "\n")
                        print "send " + self.cmd
                        self.conn.sendall(self.data1)
                        self.togle = not self.togle
                    else :
                        self.conn.sendall("msg r " + str(self.l2) + "\n")
                        print "send " + self.cmd
                        self.conn.sendall(self.data2)
                        self.togle = not self.togle
                except Exception, e :
                    print e
                    print "send errer : 1"
                finally:
                    self.lock.release()
                
        return False
                
        

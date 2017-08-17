import socket
import threading
from multiprocessing import Queue, Lock

class ServerAR(threading.Thread):

    # exception handle request
    def __init__(self, host, port, dataQueue, cmdQueue, lock):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.dataQueue = dataQueue
        self.cmdQueue = cmdQueue
        self.lock = lock
        self.cmd = 'N'
        self.isConn = False
        self.conn = None
        self.addr = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(1)

    def __del__(self):
        self.conn.close()

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
            while 1:
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
                except socket.error:
                    pass
                except Exception, e :
                    print e
                    self.cout("recv errer : 1")
                    self.isConn = False
                    #drone.stop()
                    break
                
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
                self.conn.sendall("msg r\n")
                self.cout("send " + self.cmd)

                f = open('20122314.jpg','rb')# open file as binary
                data = f.read()
                self.conn.sendall(data)
                f.flush()
                f.close()
                
        return False
                
        

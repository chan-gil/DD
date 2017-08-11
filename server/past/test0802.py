import threading
from multiprocessing import Queue

class ServerAR():

    # exception handle request
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __del__(self):
        self.conn.close()

    def recv(self, q):
        q.put('a')
        a = q.get()
        print a
        q.close()
        q.join_thread()


if __name__ == '__main__':
    q = Queue()
    server = ServerAR('192.168.123.1', 9006)
    s = threading.Thread(target=server.recv, args = (q,))
    s.start()

    #q.close()
    #q.join_thread()

    s.join()

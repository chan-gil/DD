import socket

HOST = '127.0.0.1' # server host ip
PORT = 56788 # server port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.sendall('Hello, world') #send string to server
data = s.recv(1024) #receive string from server

s.close()

print 'Received', repr(data)
print 'Received', data

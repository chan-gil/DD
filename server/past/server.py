import socket

HOST = '192.168.123.1' 
PORT = 9001 # server port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket family, socket type
                    #AF_INET : IPv4
                    #SOCK_STREAM : TCP socket
s.bind((HOST, PORT))

s.listen(1) # maximum client : 1

conn, addr = s.accept() #accept client

print 'Connected by', addr

while 1:
    data = conn.recv(1024) #recieve message
    data = data.replace('\n', '')
    msg = data.split()
    print msg
    if msg[0] == 'msg':
        if msg[1] == '200':
            break
    
    #conn.sendall(data)
    
conn.close()

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.123.1', 10003))
s.listen(1)
s.settimeout(3)
conn, addr = s.accept() #accept client


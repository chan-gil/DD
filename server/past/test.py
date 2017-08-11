import cv2
import socket
import sys
from PIL import Image
import cStringIO
'''
print '1'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print '2'
try:
    s.connect(('192.168.1.1',5555))
except Exception as e:
    print 'connection fail'
    sys.exit()
print '3'
data = s.recv(1024)
data2 = s.recv(1024)
data3 = s.recv(1024)
print '4'
print data
print '4-1'
print data2
#print '4-2'
#print data3
print '5'
f = open("img",'w')
f.write(data)
f.write('esham')
f.write(data2)
f.write('esham')
f.write(data3)
f.close()
im = Image.open(cStringIO.StringIO(data2))
im.thumbnail((40,70), Image.ANTIALIAS)
output = image
screen.blit(output,(0,0))
print '5-2'
s.close()
print '6'
'''

cam = cv2.VideoCapture('tcp://192.168.1.2:5555')
running = True
while running:
    # get current frame of video
    running, frame = cam.read()
    print cam
    print cam.isOpened()
    if running:
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == 27: 
            # escape key pressed
            running = False
    else:
        # error reading frame
        print 'error reading video feed'
cam.release()
cv2.destroyAllWindows()

'''img = cv2.imread("20122314.jpg",cv2.IMREAD_COLOR)
cv2.imshow("Image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

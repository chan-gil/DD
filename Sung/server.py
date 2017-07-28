import socket
import ARDroneLib
import sys

global drone

HOST = '192.168.123.1' 
PORT = 9005 # server port

# drone connction
try:
    drone = ARDroneLib.Drone("192.168.1.2")
except IOError:
    wait = raw_input("-> Cannot connect to drone !\n-> Press return to quit...")
    sys.exit()

# server wait
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket family, socket type
                        #AF_INET : IPv4
                        #SOCK_STREAM : TCP socket
    s.bind((HOST, PORT))

    s.listen(1) # maximum client : 1
except Exception, e:
    print e
    print "connection error : 1"
    sys.exit()

# server connection
while 1:
    try:
        conn, addr = s.accept() #accept client
        print 'Connected by', addr
    except Exception, e :
        print e
        print "connection error : 2"
        sys.exit()

# server run
    while 1:
        try :
            data = conn.recv(1024) #recieve message
            msg = data.split()
            print msg
            if msg[0] == 'msg':
                #if msg[1] == "0": #drone.emergency()
                if msg[1] == '8':
                    print "hover"
                    drone.hover()
                if msg[1] == '100':
                    print "take off"
                    drone.takeoff()
                if msg[1] == '101':
                    print "land"
                    drone.land()
                if msg[1] == '1':
                    print "forward"
                    drone.forward()
                if msg[1] == '4':
                    print "backward"
                    drone.backward()
                if msg[1] == '3':
                    print "left"
                    drone.left()
                if msg[1] == '5':
                    print "right"
                    drone.right()
                if msg[1] == '0':
                    print "left spin"
                    drone.rotate_left()
                if msg[1] == '2':
                    print "right spin"
                    drone.rotate_right()
                #if msg[1] == "8": #drone.calibrate()
                #if msg[1] == "a": #drone.reset()
                #if msg[1] == "b": #drone.set_config(activate_navdata=True)
                if msg[1] == '200': raise

                
        except Exception, e :
            print e
            print "recv errer : 1"
            #drone.stop()
            wait = raw_input("press q to exit or continue : ")
            if wait == 'q':
                sys.exit()
            break
        
    
    #conn.sendall(data)
    
conn.close()

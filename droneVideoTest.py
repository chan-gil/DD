import cv2
import libardrone

rec = False
running = True

def main():
    print '''
    usage
    r : recording (on/off)
    q : exit
    '''
    global running, rec
    cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
    drone = libardrone.ARDrone()
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('output.avi', fourcc, 24.0, (640,360))

    while (running):
        # get current frame of video
        running, frame = cam.read()
        if running:
            bat = drone.navdata.get(0, dict()).get('batery', 0)
            bet_info = 'Battery: %i%%' %bat
            cv2.putText(frame, bet_info, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            keyHandler(key)
            if rec == True:
                out.write(frame)
        else:
            print 'error reading video feed'
            break

    cam.release()
    out.release()
    cv2.destroyAllWindows()
    print "Shutting down...",
    drone.halt()
    print "Ok."

def keyHandler(key):
    global running, rec
    if key&0xFF == ord('q'):
        running = False
    elif key&0xFF == ord('r'):
        rec = not rec
        if rec:
            print 'start recording'
        else:
            print 'stop recording'
    # elif key == 13:     # return
    #     drone.takeoff()
    # elif key == 32:     # space
    #     drone.land()
    # else:
    #     drone.hover()



if __name__=='__main__':
    main()
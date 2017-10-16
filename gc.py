
x = 0
y = 0

def test(x, y = 1, z = 0):
	print x, y, z

test(3, z = 7)







print 'done'


navdata

{
 'unsupported_option': [(1, 8), (2, 52), (3, 46), (4, 16), (5, 12), (6, 88), (7, 16), (8, 24), (9, 92), (10, 56), (11, 16), (12, 44), (13, 92), (14, 108), (15, 364), (17, 8), (18, 40), (19, 65), (20, 12), (21, 18), (22, 83), (23, 64), (24,72), (25, 32), (26, 8), (28, 6), (29, 32)],
 'gps_info': {'elevation': 0.0, 'hdop': 0.0, 'data_available': 0, 'longitude': 0.0, 'zero_validated': 0, 'latitude': 0.0, 'wpt_validated': 0}, 
 'vision_detect': {'distance': 0, 'xc': 0, 'yc': 0, 'height': 0, 'width': 0, 'nb_detected': 0},
 'drone_state': {'acq_thread_on': 1, 'fw_new': 0, 'navdata_demo': 0, 'adc_watchdog': 0, 'com_lost': 0, 'ctrl_watchdog': 0, 'video_thread_on': 1, 'ultrasound_ok': 0, 'flying': 0, 'altitude_algo': 0, 'fw_update': 0, 'cutout': 0, 'angle_algo': 0, 'emergency': 0, 'too_much_angle': 0, 'command_ack': 1, 'atcodec_thread_on':1, 'pic_version_ok': 1, 'user_feedback': 0, 'navdata_thread_on': 1, 'user_emergency': 0, 'com_watchdog': 0, 'vbat_low':0, 'video_on': 0, 'motor_status': 0, 'fw_ok': 1, 'navdata_bootstrap': 0, 'vision_on': 0, 'timer_elapsed': 0},
 'navdata_demo': {'battery_percentage': 56, 'phi': 0, 'psi': 0.0, 'altitude': 0, 'ctrl_state': 0, 'vx': 0, 'vy': 0, 'vz': 0, 'theta': 0}
 }


 

    def boundCheck2(self, flag, x, y):
        if flag == -1:
            if not lastCoords:
                self.dataQueue.put('8')
                return
            else:
                count = 0
                for i in range(10):
                    if not lastXY[i] == None:
                        count = count - 1
                if count <= 5:
                    lastCoords = True
                
                
        else:
            if not lastCoords:
                count = 10
                for i in range(10):
                    if not lastXY[i] == None:
                        count = count - 1
                if count <= 0:
                    lastCoords = True
                
            lastXY[lastIndex] = x
            lastIndex = lastIndex + 1
            if lastIndex == 10:
                lastIndex = 0

            x1, y1 = self.p2fRectPoints[0] # left top
            x2, y2 = self.p2fRectPoints[2] # right bottom
            a = abs(x1 - x2) # x length
            b = abs(y1 - y2) # y length
            r = a / b # ratio

            s = a * b # box size
            print "size : " + str(s) + "ratio : " + str(r)
    
            if x < self.windowX1:
                self.dataQueue.put('3') # left
                self.dataQueue.put('0') # left spin
                self.dataQueue.put('0') # left spin
                self.dataQueue.put('0') # left spin
                self.dataQueue.put('0') # left spin
                self.dataQueue.put('0') # left spin
                # return
            elif x > self.windowX2:            
                self.dataQueue.put('5') # left
                self.dataQueue.put('2') # rignt spin
                # return
            else:
                self.dataQueue.put('8')
                # return

                
            if s < self.baseS:
                self.dataQueue.put('1') # forward




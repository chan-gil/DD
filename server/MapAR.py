import folium
import os
import time
from selenium import webdriver
from multiprocessing import Process, Queue, Lock, Event

# lat_long = [37.495705, 126.956279]
# delay = 1.5
# fn='testmap.html'
# tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)

# m = folium.Map(lat_long, zoom_start=20, tiles='Stamen Toner')
# folium.Marker(lat_long, popup='test_section').add_to(m)

# m.save(fn)

# browser = webdriver.Chrome()
# # browser = webdriver.Firefox()
# browser.get(tmpurl)
# # #Give the map tiles some time to load
# time.sleep(delay)
# browser.save_screenshot('map.png')
# browser.quit()

delay = 1.5
gpsCoord = [None] * 2
fn='testmap.html'
tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)

class MapAR():
	def __init__(self, locationQueue, mapQueue):
		self.locationQueue = locationQueue
		self.mapQueue = mapQueue

	def mapping(self):
		while(True):
			if not self.locationQueue.empty():
				gpsCoord[0], gpsCoord[1] = self.locationQueue.get()
				if gpsCoord[0] == 'q':
					break
				myMap = folium.Map(gpsCoord, zoom_start = 18, tiles = 'Stamen Toner')
				folium.Marker(gpsCoord).add_to(myMap)
				myMap.save(fn)
				browser = webdriver.Chrome()
				# browser = webdriver.Firefox()
				browser.get(tmpurl)
				# #Give the map tiles some time to load
				time.sleep(delay)
				browser.save_screenshot('map.jpeg')
				browser.quit()

		        # f1 = open('map.png','rb')# open file as binary
		        # data1 = self.f1.read()
		        # f1.flush()
		        # f1.close()
		        # mapQueue.put(data1)
			else:
				print 'no data'
				pass
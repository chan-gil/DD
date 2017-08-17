import os, sys


f = open('shot.png', "rb")
dataRaw = f.read()
f.close()
print len(dataRaw)
print '%16d' %sys.getsizeof(dataRaw)
print '%16d' %os.path.getsize("shot.png")
print os.stat("shot.png").st_size

import cv2
import numpy as np

SCALAR_RED = (0.0, 0.0, 255.0)

def main():
	first = True
	cam = cv2.VideoCapture(0)
	methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
	try:
		template = cv2.imread('testImg.png', 0)
		w, h = template.shape[::-1]
	except:
		print "fail to open target image"

	while True:
		ret, img = cam.read()
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
		
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		top_left = min_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)
		cv2.rectangle(img, top_left, bottom_right, 255, 2)
		
		if cv2.waitKey(1) == ord('q'):
			break
		cv2.imshow("frame", img)

	cv2.destroyAllWindows()
	cam.release()

###################################################################################################
if __name__ == "__main__":
    main()
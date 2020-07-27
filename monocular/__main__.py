from . import estimate

import cv2
from time import time

def capture():

	# open camera
    cap = cv2.VideoCapture(701)

    # set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while cap.isOpened():

        # read image
        ret, img = cap.read()
        if ret != True:
            print('read image failed')
            continue

		# pose estimate
        estimate.pose(img)

		# show image
        cv2.imshow('camera', img)
        key = cv2.waitKey(delay = 2)

		# save image
        if key == ord('t'):
            name = str(round(time() * 1000)) + '.jpg'
            cv2.imwrite('./assets/img/' + name, img)

		# quit
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

capture()

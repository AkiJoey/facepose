from . import estimate

import cv2
from time import time

def capture():

	# open camera
    cap = cv2.VideoCapture(700)

    # set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while cap.isOpened():

        # read image
        ret, img = cap.read()
        if ret != True:
            print('read image failed')
            continue

		# cut image
        img1 = img[:, 0:640, :]
        img2 = img[:, 640:1280, :]

        # pose estimate
        estimate.pose(img1, img2)
        estimate.depth(img1, img2)

        # show image
        cv2.imshow('left', img1)
        cv2.imshow('right', img2)
        key = cv2.waitKey(delay = 2)

		# save image
        if key == ord('t'):
            name = str(round(time() * 1000)) + '.jpg'
            cv2.imwrite('./assets/img1/' + name, img1)
            cv2.imwrite('./assets/img2/' + name, img2)

		# quit
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

capture()

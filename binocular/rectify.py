from . import setting

import cv2

def stereo(img1, img2, size):

	# read config
	mtx1, dist1, mtx2, dist2, rvecs, tvecs = setting.read()

	# stereo rectify
	R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
		mtx1, dist1, mtx2, dist2, size, rvecs, tvecs, alpha = 0
	)
	map1x, map1y = cv2.initUndistortRectifyMap(mtx1, dist1, R1, P1, size, cv2.CV_32FC1)
	map2x, map2y = cv2.initUndistortRectifyMap(mtx2, dist2, R2, P2, size, cv2.CV_32FC1)

	# distortion rectify
	img1 = cv2.remap(img1, map1x, map1y, cv2.INTER_LINEAR)
	img2 = cv2.remap(img2, map2x, map2y, cv2.INTER_LINEAR)

	return img1, img2, Q

def distort(img, mtx, dist):
	img = cv2.undistort(img, mtx, dist)
	return img

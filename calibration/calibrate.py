from . import setting

import cv2
import numpy as np

def calibrate(width, height, img_list, size):

	# corners criteria
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	
	# chessboard corners
	objp = np.zeros((width * height, 3), np.float32)
	objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

	# world coordinate and pixel coordinate
	obj_points = []
	img_points = []

	for img_path in img_list:
		img = cv2.imread(img_path)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# find chessboard corners
		ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

		# save chessboard corners
		if ret is True:
			cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
			obj_points.append(objp)
			img_points.append(corners)

	# calibrate camera
	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)

	# reprojection error
	total_error = 0
	for i in range(len(obj_points)):
		img_points2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], mtx, dist)
		error = cv2.norm(img_points[i], img_points2, cv2.NORM_L2) / len(img_points2)
		total_error += error
	average_error = total_error / len(obj_points)

	return mtx, dist, average_error

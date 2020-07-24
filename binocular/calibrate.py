from . import setting

import cv2
import numpy as np
from glob import glob

def calibrate(width, height, img_list)

	# 棋盘格角点的参数 最大循环次数为 30 最大误差容限为 0.001
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	
	# 世界坐标系中的棋盘格角点 (二维矩阵)
	objp = np.zeros((width * height, 3), np.float32)
	objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

	# 棋盘格角点的世界坐标和图像坐标
	obj_points = []	# 世界坐标
	img_points = []	# 图像坐标

	for img_path in img_list:
		img = cv2.imread(img_path)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		size = gray.shape[::-1]

		# 寻找棋盘格角点
		ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

		# 保存棋盘格角点
		if ret is True:
			cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
			obj_points.append(objp)
			img_points.append(corners)
			# 将角点在图像上显示
			cv2.drawChessboardCorners(img, (width, height), corners, ret)
			cv2.imshow('findCorners', img)
			cv2.waitKey(1)
	cv2.destroyAllWindows()

	# 内参标定
	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)

	# 反投影误差
	total_error = 0
	for i in range(len(obj_points)):
		img_points2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], mtx, dist)
		error = cv2.norm(img_points[i], img_points2, cv2.NORM_L2) / len(img_points2)
		total_error += error
	print("average error: ", total_error / len(obj_points))

	return size, obj_points, img_points, mtx, dist

	
def main():

	# 单目标定
	size, obj_points, img_points1, mtx1, dist1 = calibrate(7, 7, glob('../assets/left/*.jpg'))
	size, obj_points, img_points2, mtx2, dist2 = calibrate(7, 7, glob('../assets/right/*.jpg'))

	# 双目标定
	ret, mtx1, dist1, mtx2, dist2, rvecs, tvecs = cv2.stereoCalibrate(
		obj_points, img_points1, img_points2, mtx1, dist1, mtx2, dist2, size, flags = cv2.CALIB_USE_INTRINSIC_GUESS
	)

	# 将标定参数写入配置文件
	setting.write(mtx1, dist1, mtx2, dist2, rvecs, tvecs)

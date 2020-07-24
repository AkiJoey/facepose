import cv2
import numpy as np

def disparity_BM(img1, img2):

	# 两个 trackbar 用来调节不同的参数查看效果
    num = cv2.getTrackbarPos("num", "depth")
    blockSize = cv2.getTrackbarPos("blockSize", "depth")
    if blockSize % 2 == 0:
        blockSize += 1
    if blockSize < 5:
        blockSize = 5

	stereo = cv2.StereoBM_create(numDisparities = num * 16, blockSize = blockSize)
	disparity = stereo.compute(img1, img2)

	disp = cv2.normalize(
        disparity, disparity, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U
    )
	disp = np.divide(disp.astype(np.float32), 16.)

	return disp

def disparity_SGBM(img1, img2):

	# SGBM 匹配参数设置
	if left_image.ndim == 2:
		img_channels = 1
	else:
		img_channels = 3
	blockSize = 3
	param = {
		'minDisparity': 0,
		'numDisparities': 128,
		'blockSize': blockSize,
		'P1': 8 * img_channels * blockSize ** 2,
		'P2': 32 * img_channels * blockSize ** 2,
		'disp12MaxDiff': 1,
		'preFilterCap': 63,
		'uniquenessRatio': 15,
		'speckleWindowSize': 100,
		'speckleRange': 1,
		'mode': cv2.STEREO_SGBM_MODE_SGBM_3WAY
	}

	stereo = cv2.StereoSGBM_create(**param)
	disparity = stereo.compute(img1, img2)
	disp = np.divide(disparity.astype(np.float32), 16.)

	return disp

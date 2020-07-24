from . import estimate

import cv2
import numpy as np
from time import time

# 打开双目摄像头
def capture():

	# 打开摄像头
    cap = cv2.VideoCapture(1)

    # 设置分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while cap.isOpened():

        # read frame
        ret, frame = cap.read()
        if ret != True:
            print('read frame failed')
            continue
        size = frame.shape[::-1]
        print(size)

		# 左右图像切割
        img1 = frame[:, 0:640, :]
        img2 = frame[:, 640:1280, :]

        estimate.distance(img1, img2)

        def callback(e, x, y, f, p):
            if e == cv2.EVENT_LBUTTONDOWN:        
                print(threeD[y][x])
        cv2.setMouseCallback('depth', callback, None)

        if ret:

            # 显示图像
            cv2.imshow('left', img1)
            cv2.imshow('right', img2)

        key = cv2.waitKey(delay = 2)

		# 按 t 保存图片
        if key == ord('t'):
            name = str(round(time() * 1000)) + '.jpg'
            cv2.imwrite('./assets/img1/' + name, img1)
            cv2.imwrite('./assets/img2/' + name, img2)

		# 按 q 退出
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

capture()

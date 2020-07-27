from . import setting
from . import landmark
from . import convert

from . import rectify
from . import matching

import cv2

def process(img1, img2):

    # gray scale image
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # histogram equalization
    img1 = cv2.equalizeHist(img1)
    img2 = cv2.equalizeHist(img2)

    return img1, img2

def depth(img1, img2):

    # image size
    size = (img1.shape[1], img1.shape[0])

    # 立体校正及畸变校正, Q 为投影矩阵
    img1, img2, Q = rectify.stereo(img1, img2, size)

    # process image
    gray1, gray2 = process(img1, img2)

    # 立体匹配, 获取视差图
    disp = matching.disparity_SGBM(gray1, gray2)
    cv2.imshow('depth', disp)
    
    # 计算 3D 坐标, z 轴即为深度
    threeD = cv2.reprojectImageTo3D(disp, Q)
    def callback(e, x, y, f, p):
        if e == cv2.EVENT_LBUTTONDOWN:
            print(threeD[y][x])
    cv2.setMouseCallback('depth', callback, None)

def pose(img1, img2):

    # read config
    mtx1, dist1, mtx2, dist2, rvecs, tvecs = setting.read()

    # process image
    gray1, gray2 = process(img1, img2)

    # face points detect
    obj_points, img_points = landmark.detect(gray1)
    if obj_points is None:
        return

    # core algorithm
    ret, rvecs, tvecs = cv2.solvePnP(
        obj_points, img_points, mtx1, dist1, flags = cv2.SOLVEPNP_ITERATIVE
    )
    
    # convert degree and distance
    pitch, yaw, roll = convert.degree(rvecs)
    distance = convert.distance(tvecs)

    # draw face points
    for p in img_points:
        cv2.circle(img1, (int(p[0]), int(p[1])), 3, (0, 0, 255), 1)

    # draw pose info
    distance_str = 'distance: {}'.format(round(distance, 2))
    euler_angle_str = 'pitch: {}, yaw: {}, roll: {}'.format(pitch, yaw, roll)
    cv2.putText(img1, euler_angle_str, (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
    cv2.putText(img1, distance_str, (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

from . import setting
from . import landmark
from . import convert

import cv2

def process(img):

    # gray scale image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # histogram equalization
    img = cv2.equalizeHist(img)

    return img

def pose(img):

    # read config
    mtx, dist = setting.read()
    if mtx.all() is None:
        return

    # face points detect
    obj_points, img_points = landmark.detect(process(img))
    if obj_points is None:
        return

    # core algorithm
    ret, rvecs, tvecs = cv2.solvePnP(
        obj_points, img_points, mtx, dist, flags = cv2.SOLVEPNP_ITERATIVE
    )

    # convert degree and distance
    pitch, yaw, roll = convert.degree(rvecs)
    distance = convert.distance(tvecs)

    # draw face points
    for p in img_points:
        cv2.circle(img, (int(p[0]), int(p[1])), 3, (0, 0, 255), 1)

    # draw pose info
    distance_str = 'distance: {}'.format(round(distance, 2))
    euler_angle_str = 'pitch: {}, yaw: {}, roll: {}'.format(pitch, yaw, roll)
    cv2.putText(img, euler_angle_str, (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
    cv2.putText(img, distance_str, (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

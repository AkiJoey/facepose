import cv2
import math

def degree(rvecs):

    # calculate rotation angles
    theta = cv2.norm(rvecs, cv2.NORM_L2)
    
    # transformed to quaterniond
    w = math.cos(theta / 2)
    x = math.sin(theta / 2) * rvecs[0][0] / theta
    y = math.sin(theta / 2) * rvecs[1][0] / theta
    z = math.sin(theta / 2) * rvecs[2][0] / theta

    # pitch (x-axis rotation)
    t0 = 2.0 * (w * x + y * z)
    t1 = 1.0 - 2.0 * (x * x + y * y)
    pitch = math.atan2(t0, t1)
    
    # yaw (y-axis rotation)
    t2 = 2.0 * (w * y - z * x)
    if t2 > 1.0:
        t2 = 1.0
    if t2 < -1.0:
        t2 = -1.0
    yaw = math.asin(t2)
    
    # roll (z-axis rotation)
    t3 = 2.0 * (w * z + x * y)
    t4 = 1.0 - 2.0 * (y * y + z * z)
    roll = math.atan2(t3, t4)
    
	# radian to degree
    X = int((pitch / math.pi) * 180)
    Y = int((yaw / math.pi) * 180)
    Z = int((roll / math.pi) * 180)
    
    return X, Y, Z

def distance(tvecs):
    return -tvecs[2][0]

from . import setting
from . import calibrate

import glob

# image size
size = (640, 480)

# monocular calibration
images = glob.glob('./assets/img/*.jpg')
mtx, dist, error = calibrate.calibrate(7, 7, images, size)

# print calibration
print("average error: ", error)
print('mtx: ', mtx)
print('dist: ', dist)

# write config
setting.write(mtx, dist)

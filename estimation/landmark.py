import os
import cv2
import dlib
import numpy as np

# get predictor path
assets_path = os.getcwd() + '/assets/'
predictor_path = assets_path + 'shape_predictor_68_face_landmarks.dat'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
POINTS_NUM_LANDMARK = 68

def largest(dets):
    if len(dets) == 1:
        return dets[0]

    areas = [(det.right() - det.left()) * (det.bottom() - det.top()) for det in dets]

    max_index = 0
    max_area = areas[0]
    for index in range(1, len(dets)):
        if areas[index] > max_area:
            max_index = index
            max_area = areas[index]

    return dets[max_index]

def predict(landmark_shape):
    if landmark_shape.num_parts != POINTS_NUM_LANDMARK:
        print("ERROR: landmark_shape.num_parts-{}".format(landmark_shape.num_parts))
        return None, None

    # object points
    obj_points = np.array([
        (6.825897, 6.760612, 4.402142),     #33 left brow left corner
        (1.330353, 7.122144, 6.903745),     #29 left brow right corner
        (-1.330353, 7.122144, 6.903745),    #34 right brow left corner
        (-6.825897, 6.760612, 4.402142),    #38 right brow right corner
        (5.311432, 5.485328, 3.987654),     #13 left eye left corner
        (1.789930, 5.393625, 4.413414),     #17 left eye right corner
        (-1.789930, 5.393625, 4.413414),    #25 right eye left corner
        (-5.311432, 5.485328, 3.987654),    #21 right eye right corner
        (2.005628, 1.409845, 6.165652),     #55 nose left corner
        (-2.005628, 1.409845, 6.165652),    #49 nose right corner
        (2.774015, -2.080775, 5.048531),    #43 mouth left corner
        (-2.774015, -2.080775, 5.048531),   #39 mouth right corner
        (0.000000, -3.116408, 6.097667),    #45 mouth central bottom corner
        (0.000000, -7.415691, 4.070434)     #6 chin corner
    ])
    
    # image points
    img_points = np.array([
        (landmark_shape.part(17).x, landmark_shape.part(17).y), #17 left brow left corner
        (landmark_shape.part(21).x, landmark_shape.part(21).y), #21 left brow right corner
        (landmark_shape.part(22).x, landmark_shape.part(22).y), #22 right brow left corner
        (landmark_shape.part(26).x, landmark_shape.part(26).y), #26 right brow right corner
        (landmark_shape.part(36).x, landmark_shape.part(36).y), #36 left eye left corner
        (landmark_shape.part(39).x, landmark_shape.part(39).y), #39 left eye right corner
        (landmark_shape.part(42).x, landmark_shape.part(42).y), #42 right eye left corner
        (landmark_shape.part(45).x, landmark_shape.part(45).y), #45 right eye right corner
        (landmark_shape.part(31).x, landmark_shape.part(31).y), #31 nose left corner
        (landmark_shape.part(35).x, landmark_shape.part(35).y), #35 nose right corner
        (landmark_shape.part(48).x, landmark_shape.part(48).y), #48 mouth left corner
        (landmark_shape.part(54).x, landmark_shape.part(54).y), #54 mouth right corner
        (landmark_shape.part(57).x, landmark_shape.part(57).y), #57 mouth central bottom corner
        (landmark_shape.part(8).x, landmark_shape.part(8).y),   #8 chin corner
    ], dtype = 'double')

    return obj_points, img_points

def detect(img):

    # detect face
    dets = detector(img, 0)
    if len(dets) == 0:
        return None, None
    face = largest(dets)
    
    # predict points
    landmark_shape = predictor(img, face)
    obj_points, img_points = predict(landmark_shape)

    return obj_points, img_points

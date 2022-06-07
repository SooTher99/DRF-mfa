import dlib
from django.conf import settings
import os


def get_sp_facerec_detector():
    sp = dlib.shape_predictor(os.path.join(settings.DLIB_ROOT, 'shape_predictor_68_face_landmarks.dat'))
    facerec = dlib.face_recognition_model_v1(os.path.join(settings.DLIB_ROOT,
                                                          'dlib_face_recognition_resnet_model_v1.dat'))
    detector = dlib.get_frontal_face_detector()
    return sp, facerec, detector

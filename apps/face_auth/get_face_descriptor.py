from skimage import io
from dlib_file.dlib_load import get_sp_facerec_detector


def get_descriptor(photo_path):
    global shape
    photo = io.imread(photo_path)
    sp, facerec, detector = get_sp_facerec_detector()
    dets = detector(photo, 1)
    for k, d in enumerate(dets):
        shape = sp(photo, d)
    face_descriptor = facerec.compute_face_descriptor(photo, shape)

    return list(face_descriptor)

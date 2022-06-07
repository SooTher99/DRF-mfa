import dlib
from skimage import io
from scipy.spatial import distance
#загружаем сверточные нейросети с официального сайта dlib 
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
#сверточная нейросеть выделения на фотографии лица с помощью 68 ключевых точек 
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
#сверточная нейросеть выделяющая дискриптор из лиц 
detector = dlib.get_frontal_face_detector()

#загружаем первую фотографию 
img = io.imread('pasha1.jpg')

#показываем фотогрфию средствами dlib
win1=dlib.image_window()
win1.clear_overlay()
win1.set_image(img)

#находим лицо на фотографии 
dets = detector(img, 1)
for k, d in enumerate(dets):
    print("Detection {}: Left: {} Top: {} Right: {} Button: {}".format( 
        k, d.left(), d.top(), d.right(), d.bottom()))
    shape = sp(img,d)
    win1.clear_overlay()
    win1.add_overlay(d)
    win1.add_overlay(shape)
    
#извлекаем дискриптор из лица 
face_descriptor1= facerec.compute_face_descriptor(img, shape)
#печатаем дискриптор 
print(face_descriptor1)
print("")

#те же дейстивия делаем и со вторым фото, загружаем и обрабатываем 
img2 = io.imread('pasha2.jpg')
win2=dlib.image_window()
win2.clear_overlay()
win2.set_image(img2)
dets = detector(img2, 1)
for k, d in enumerate(dets):
    print("Detection {}: Left: {} Top: {} Right: {} Button: {}".format( 
        k, d.left(), d.top(), d.right(), d.bottom()))
    shape = sp(img2,d)
    win2.clear_overlay()
    win2.add_overlay(d)
    win2.add_overlay(shape)
face_descriptor2= facerec.compute_face_descriptor(img2, shape)
print(face_descriptor2)

#рассчитываем евклидово расстояние между двумя дексрипторами лиц
#в dlib рекомендуется использовать граничное значение евклидова расстояния
#между дескрипторами лиц равное 0.6. Если Евклидово расстояние меньше 0.6, 
#значит фотографии принадлежат одному человеку.

#но в моем случае, 0.6 не является объективным значением и я буду использовать 
#значение 0.551  
a = distance.euclidean(list(face_descriptor1), list(face_descriptor2))
#выводим евклидова растояния
print(a)
if a < 0.551:
    print('Это один и тот же человек')
else:
    print('Это другой человек')


import cv2, numpy, os
from rest_framework.response import Response
from rest_framework import status



face_cap = cv2.CascadeClassifier('face_recog/haarcascade_frontalface_default.xml')
datasets = 'face_recog/datasets/'  
video_cap = cv2.VideoCapture(0)
size = 4

def face_store(name):
# These are sub data sets of folder for faces 
    sub_data = name

    path = os.path.join(datasets, sub_data)
    if not os.path.isdir(path):
        os.mkdir(path)
    
    # defining the size of images 
    (width, height) = (130, 100)    

    
    # The program loops until it has 30 images of the face.
    count = 0
    while count < 30: 
        (_, cap_data) = video_cap.read()
        col = cv2.cvtColor(cap_data, cv2.COLOR_BGR2GRAY)
        faces = face_cap.detectMultiScale(col, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(cap_data, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = col[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            cv2.imwrite('% s/% s.png' % (path, count), face_resize)
        count += 1
        
        cv2.imshow('Reading your image', cap_data)
        if cv2.waitKey(100) == ord("z"):
            break

    return Response({
        'message': "Your face is stored for future Logins"
    }, status=status.HTTP_200_OK)
# It helps in identifying the faces

  
def face_identify(name):
    print('Recognizing Face Please Be in sufficient Lights...')
    
    # Create a list of images and a list of corresponding names
    (images, labels, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(datasets):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(datasets, subdir)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                label = id
                images.append(cv2.imread(path, 0))
                labels.append(int(label))
            id += 1
    (width, height) = (130, 100)
    
    # Create a Numpy array from the two lists above
    (images, labels) = [numpy.array(series) for series in [images, labels]]
    
    # Training model
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, labels)
    
    # Part 2: Use fisherRecognizer on camera stream
    while True:
        (_, cap_data) = video_cap.read()
        col = cv2.cvtColor(cap_data, cv2.COLOR_BGR2GRAY)
        faces = face_cap.detectMultiScale(col, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(cap_data, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = col[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            # Try to recognize the face
            prediction = model.predict(face_resize)
            cv2.rectangle(cap_data, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
            if prediction[1]<500:
                cv2.putText(cap_data, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
            else:
                cv2.putText(cap_data, 'not recognized', (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

            if names[prediction[0]] == name and prediction[1]>50.0:
                print("Match")
                return Response({
                    'message': "Face Match",
                    'identified': True,
                }, status=status.HTTP_202_ACCEPTED)
            else:
                print("Cant give access sorry")
                return Response({
                    'message': "Face Not Match",
                    'identified': False,
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
        cv2.imshow('Recognizing face', cap_data)
        
        if cv2.waitKey(100) == ord("z"):
            break
        break
    




face_store('x')
face_identify('x')
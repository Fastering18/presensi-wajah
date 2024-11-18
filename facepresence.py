import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime

path = 'dataset_wajah'
file_encoded = 'data_wajah'
images = []
classNames = []
mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

def markAttendance(name):
    with open('presensi.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'{name},{time},{date}\n')

if os.path.isfile(file_encoded+".npz"):
    encoded_face_train = np.load(file_encoded+".npz")["data"]
else:
    encoded_face_train = findEncodings(images)

# testpic as fc.load_image_file
def recognize_face(testpic):
    face_locs = face_recognition.face_locations(testpic)
    picencode = face_recognition.face_encodings(testpic, face_locs)
    matches = face_recognition.compare_faces(encoded_face_train, picencode)
    faceDist = face_recognition.face_distance(encoded_face_train, picencode)
    matchIndex = np.argmin(faceDist)

    res = []
    for encode_face, faceloc in zip(picencode, face_locs):
        if matches[matchIndex]:
            name = classNames[matchIndex].upper().lower()
            res.append({'id': int(matchIndex), 'nama': name, 'lokasi': faceloc})
    
    return res
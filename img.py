import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle

path = 'dataset_meme'
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


encoded_face_train = findEncodings(images)

testpic = face_recognition.load_image_file("dataset_meme/bu_elok.jpg")
picencode = face_recognition.face_encodings(testpic)[0]
matches = face_recognition.compare_faces(encoded_face_train, picencode)
faceDist = face_recognition.face_distance(encoded_face_train, picencode)
matchIndex = np.argmin(faceDist)
print(matchIndex)
if matches[matchIndex]:
    name = classNames[matchIndex].upper().lower()
    print(name)
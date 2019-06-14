# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 03:28:28 2019

@author: kaust
"""

# It helps in identifying the faces 
import cv2,numpy, os , openpyxl
size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'
students=['']  
# Part 1: Create fisherRecognizer 
print('Recognizing Face Please Be in sufficient Lights...') 

def reset():
    wb = openpyxl.load_workbook('Attendance.xlsx')
    sheet = wb['Sheet1']
    for i in range(2,10):
        cell='B'+str(i)
        if(sheet[cell].value==False):
            break
        sheet[cell].value='A'
    wb.save('Attendance.xlsx')

def update(students):
    wb = openpyxl.load_workbook('Attendance.xlsx')
    sheet = wb['Sheet1']
    for i in range(2,5):
        cell='A'+str(i)
        if(sheet[cell].value==False):
            break
        print(sheet[cell].value)
        if(sheet[cell].value in students):
            sheet['B'+str(i)].value='P'
    wb.save('Attendance.xlsx')

# Create a list of images and a list of corresponding names 
(images, lables, names, id) = ([], [], {}, 0) 
for (subdirs, dirs, files) in os.walk(datasets): 
    for subdir in dirs: 
        names[id] = subdir 
        subjectpath = os.path.join(datasets, subdir) 
        for filename in os.listdir(subjectpath): 
            path = subjectpath + '/' + filename 
            lable = id
            images.append(cv2.imread(path, 0)) 
            lables.append(int(lable)) 
        id += 1
(width, height) = (130, 100) 
  
# Create a Numpy array from the two lists above 
(images, lables) = [numpy.array(lis) for lis in [images, lables]] 
  
# OpenCV trains a model from the images 
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, lables) 
  
# Part 2: Use fisherRecognizer on camera stream 
face_cascade = cv2.CascadeClassifier(haar_file) 
webcam = cv2.VideoCapture(0) 
while True: 
    (_, im) = webcam.read() 
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    for (x, y, w, h) in faces: 
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
        face = gray[y:y + h, x:x + w] 
        face_resize = cv2.resize(face, (width, height)) 
        # Try to recognize the face 
        prediction = model.predict(face_resize) 
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3) 
  
        if prediction[1]<100: 
  
           cv2.putText(im, '% s - %.0f' % 
(names[prediction[0]], prediction[1]), (x-10, y-10),  
cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
           if(names[prediction[0]] not in students):
               students.append(names[prediction[0]])
        else: 
          cv2.putText(im, 'not recognized',  
(x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
  
    cv2.imshow('OpenCV', im) 
      
    key = cv2.waitKey(10) 
    if key == 27:
        cv2.destroyAllWindows()
        webcam.release()
        break

update(students)

os.startfile("Attendance.xlsx")

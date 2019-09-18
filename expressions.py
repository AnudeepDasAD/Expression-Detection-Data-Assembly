#Need to collect images first
import cv2
import os
from PIL import Image
import numpy as np
import tensorflow as tf
#PIL is the Python Image Library

# Citation: R Vemulapalli, A Agarwala, “A Compact Embedding for Facial Expression Similarity”, CoRR, abs/1811.11283, 2018.

import pickle
#Pickle is used to create new files

face_cascade = cv2.CascadeClassifier('/Python/Python37/cascades/data/haarcascade_frontalface_alt2.xml')

#The recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

#The current directory
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))

#Actual folder names
labels_directory = "Emotion"

images_directory= "cohn-kanade-images"

#label will be the folder's name

#joining the images_folder path
image_dir = os.path.join(BASE_DIR, labels_directory) 

current_id=0
label_ids = {"Neutral":0, "Anger":1, "Contempt":2, "Disgust":3, "Fear":4, "Happy":5, "Sadness":6, "Surprise": 7}

x_train = []
y_labels = []

#Will hold the paths to the labels because the file structure for the images is very similar
paths = []

#Walking through the directory and assembling all of the y-values
for root, dirs, files in os.walk(labels_directory):
	for file in files:
		if file.endswith("txt"):
			path = os.path.join(root, file)
			paths.append(path)
			#f = open(str(path), "r")
			with open(str(path)) as f:
				for line in f:
					line = line.strip()
					#Line is not empty
					if line:
						#print(int(float(line))) It works!
						id_ = int(float(line))
						y_labels.append(id_)
						#print(id_)

#Assembling the images and x_train

index = 0
for path in paths:
	#The first part of the relative path changes
	path = path.replace(labels_directory, images_directory)

	#The name of 
	path = path.replace("_emotion.txt", ".png")

	pil_image = Image.open(path).convert("L")	 #grayscale

	#pil_image.resize((275,275), Image.ANTIALIAS)
	#Convert the image into a numpy array
	image_array = np.array(pil_image, "uint8")

	#print(image_array.shape)

	#Ensuring all have the same shape
	if image_array.shape != (490,640):
		y_labels.pop(index)
		continue

	#Add the faces
	faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.3, minNeighbors=5)
	for (x,y,w,h) in faces:
		region_of_interest = image_array[y:y+h, x:x+w]

		#np.reshape(region_of_interest, (250,250))
		print(region_of_interest.shape)
		#print(y_labels)

		x_train.append(region_of_interest)
	index += 1
#Both are 327 elements large
print(len(x_train))
print(len(y_labels))


#Go through all of the images and process them into our x_labels
#All of the images are already grayscale


#wb is writing bytes
#Label ids and their corresponding labels are now saved 
with open("emotion_labels.pkl", "wb") as f:
	pickle.dump(label_ids, f)

#Training the data with our training data  (y_labels only has numbers) (as numpy arrays)
recognizer.train(x_train, np.array(y_labels))
recognizer.save("emotion_training.yml")

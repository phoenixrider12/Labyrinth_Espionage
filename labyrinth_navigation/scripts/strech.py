import cv2
import os

img=cv2.imread('/home/aryaman/Labyrinth_Espionage/spy/src/images/image1.png')
img2=cv2.imread('/home/aryaman/Labyrinth_Espionage/spy/src/images/image1.png').reshape(-1)
print(img)
print("Hello")
print(img2)
img3=img2.reshape(379,1049,3)
print(img3)
cv2.imshow('ext',img3)
cv2.waitKey(200)

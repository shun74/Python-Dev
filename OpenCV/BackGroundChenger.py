import cv2
import os

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(cv2.CAP_PROP_FPS, 60)
imageBg = cv2.imread("images/1.jpg")
imageBg = cv2.resize(imageBg,(640,480))

import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(cv2.CAP_PROP_FPS, 60)
segmentor = SelfiSegmentation()
fpsReader = cvzone.FPS()
imageBg = cv2.imread("images/1.jpg")
imageBg = cv2.resize(imageBg,(640,480))

while True:
    success, image = cap.read()
    image = cv2.flip(image,1)
    imageOut = segmentor.removeBG(image,imageBg,threshold=0.8)

    imageStacked = cvzone.stackImages([image,imageOut],2,1)
    _, imageStacked = fpsReader.update(imageStacked)

    cv2.imshow("Image",imageStacked)
    cv2.waitKey(1)

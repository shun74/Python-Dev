import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from FaceDetectionModule import faceDetector

detector = faceDetector(detectionCon=0.4)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        continue

    image,bboxes,landmarks,scales,scores = detector.findFace(image,draw=False)

    for bbox,landmark,scale in zip(bboxes,landmarks,scales):
        x1,x2 = int(bbox[0]),int(bbox[2])
        y1,y2 = int(bbox[1]),int(bbox[3])

        roi = image[y1:y2,x1:x2]
        image[y1:y2,x1:x2] = cv2.GaussianBlur(roi,(45,45),15)

        image_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(image_pil)
        fontpath ='C:\Windows\Fonts\HGRPP1.TTC'

        font = ImageFont.truetype(fontpath, int(scale[0]*120))
        (x,y) = landmark[0]
        draw.text((x-scale[0]*50,y-scale[1]*30), "へ", font = font , fill = (0,255,0) )
        draw.text((x-scale[0]*50,y+scale[1]*40), "の", font = font , fill = (0,255,0) )
        (x,y) = landmark[1]
        draw.text((x-scale[0]*50,y-scale[1]*30), "へ", font = font , fill = (0,255,0) )
        draw.text((x-scale[0]*50,y+scale[1]*40), "の", font = font , fill = (0,255,0) )
        font = ImageFont.truetype(fontpath, int(scale[0]*140))
        (x,y) = landmark[2]
        draw.text((x-scale[0]*70,y-scale[1]*20), "も", font = font , fill = (0,255,0) )
        font = ImageFont.truetype(fontpath, int(scale[0]*160))
        (x,y) = landmark[3]
        draw.text((x-scale[0]*70,y-scale[1]*20), "へ", font = font , fill = (0,255,0) )
        fontpath ='C:\Windows\Fonts\HGRGM.TTC'
        font = ImageFont.truetype(fontpath, int(scale[0]*850))
        (x,y) = bbox[0]+scale[0]*0.2,bbox[1]+scale[1]*0.3
        draw.text((x-scale[0]*100,y+scale[1]*100), "し", font = font , fill = (0,255,0) )
        font = ImageFont.truetype(fontpath, int(scale[0]*750))
        (x,y) = bbox[2]-scale[0]*0.1,bbox[1]+scale[1]*0.3
        draw.text((x-scale[0]*250,y+scale[1]*100), "゛", font = font , fill = (0,255,0) )
        image = np.array(image_pil)

    cv2.imshow('MediaPipe Face Detection', image)


    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()

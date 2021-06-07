import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

#########################
wCam, hCam = 640, 480
#########################

print("Loading Cam...")
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
lmList = [[] for i in range(2)]
bbox = [[] for i in range(2)]
hand = [[] for i in range(2)]
fingers = [[] for i in range(2)]
num = 0
detector = htm.handDetector(detectionCon = 0.7, maxHands=2)
print("Cam Loaded")


while True:
    success, img = cap.read()
    # Find Hand
    img = cv2.flip(img, 1)

    img, hand_rl = detector.findBothHands(img)
    if len(hand_rl) >= 2:
        hand[0] = hand_rl[0]["classification"][0]["label"]
        hand[1] = hand_rl[1]["classification"][0]["label"]
        if hand[0]=="Left":
            lmList[0], bbox[0] = detector.findPosition(img, handNo=0, draw=False)
            lmList[1], bbox[1] = detector.findPosition(img, handNo=1, draw=False)
        else:
            lmList[1], bbox[1] = detector.findPosition(img, handNo=0, draw=False)
            lmList[0], bbox[0] = detector.findPosition(img, handNo=1, draw=False)

        x1, y1 = (bbox[0][0]+bbox[0][2])//2-50, bbox[0][1]-20
        x2, y2 = (bbox[1][0]+bbox[1][2])//2, bbox[1][1]-20
        cv2.putText(img, "Left", (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (100,0,100), 3)
        cv2.putText(img, "Right", (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (0,100,100), 3)

        fingers[0] = detector.areFingersUp(lmList[0])
        fingers[1] = detector.areFingersUp(lmList[1])

        num = 0
        for i in range(5):
            num += 2**(i+5) * fingers[0][i]
            num += 2**i * fingers[1][4-i]

        cv2.putText(img, f"{num}", (300, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,0) ,3)


    # Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

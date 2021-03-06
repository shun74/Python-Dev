import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#########################
wCam, hCam = 640, 480
#########################

print("Loading Cam...")
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon = 0.7, maxHands=1)
print("Cam Loaded")

# Pycaw setting
print("Loading Audio...")
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-40, None)
minVol = volRange[0] + 10
maxVol = volRange[1]
vol = minVol
volBar = 400
volPer = 0
colorVol = (0, 255, 0)
print("Audio Loaded")

while True:
    success, img = cap.read()
    # Find Hand
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)
    if len(lmList) > 0:

        # Filter based on size
        area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1]) // 100
        if 250<area<1000:
            #Find Distance between index and Thumb
            length, img, lineinfo = detector.findDistance(4,8,img)
            #Convert Volume
            volBar = np.interp(length,[50,300],[400,150])
            volPer = np.interp(length,[50,300],[0,100])
            # Reduce Resolution to make it smoother
            smoothness = 2
            volPer = smoothness * round(volPer/smoothness)
            # Check fingers up
            fingers = detector.fingersUp()
            # if pinky down set volume
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer/100, None)
                cv2.circle(img, (lineinfo[4],lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

    # Drawings
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f"Vol: {int(volPer)} %", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cVol = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(img, f"Vol Set: {int(cVol)}", (400, 50), cv2.FONT_HERSHEY_COMPLEX, 1, colorVol, 3)

    # Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

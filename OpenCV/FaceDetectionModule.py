import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

class faceDetector():
    def __init__(self, detectionCon=0.5):
        self.detectionCon = detectionCon

        self.mpFaces = mp.solutions.face_detection
        self.faces = self.mpFaces.FaceDetection(min_detection_confidence=self.detectionCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findFace(self, image, draw=False):
        bboxes = list()
        landmarks = list()
        scales = list()
        scores = list()

        imageFlipedRGB = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
        imageFlipedRGB.flags.writeable = False
        self.results = self.faces.process(imageFlipedRGB)
        imageFlipedRGB.flags.writeable = True
        image = cv2.cvtColor(imageFlipedRGB, cv2.COLOR_RGB2BGR)

        if self.results.detections:
            for detection in self.results.detections:
                if draw:
                    self.mpDraw.draw_detection(image,detection)

                info_dict = (MessageToDict(detection))

                scores.append(info_dict["score"])

                window_y,window_x,_ = image.shape
                bbox = info_dict["locationData"]["relativeBoundingBox"]

                scales.append([bbox["width"],bbox["height"]])

                bboxes.append([bbox["xmin"]-bbox["width"]*0.2,bbox["ymin"]-bbox["height"]*0.3,
                bbox["xmin"]+bbox["width"]*1.1,bbox["ymin"]+bbox["height"]*1.1])
                for i in range(4):
                    if i%2==0:
                        bboxes[-1][i] = max(0,min(1,bboxes[-1][i]))*window_x
                    else:
                        bboxes[-1][i] = max(0,min(1,bboxes[-1][i]))*window_y
                landmark = list()
                for loc in info_dict["locationData"]["relativeKeypoints"]:
                    landmark.append((int(loc["x"]*window_x),int(loc["y"]*window_y)))
                landmarks.append(landmark)
        return image, bboxes, landmarks, scales, scores

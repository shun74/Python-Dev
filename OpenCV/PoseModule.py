import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

class poseDetector():
    def __init__(self,detectionCon=0.6,trackingCon=0.6):
        self.mpDraw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackingCon
        )

    def findPose(self, img, draw=True):
        img.flags.writeable = False
        results = self.pose.process(img)

        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if draw:
            self.mpDraw.draw_landmarks(
                img,results.pose_landmarks,self.mp_pose.POSE_CONNECTIONS)

        landmarks = MessageToDict(results.pose_landmarks)["landmark"]

        return img, landmarks

if __name__ == '__main__':
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    poseDetection = poseDetector(detectionCon=0.6,trackingCon=0.6)

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        image, landmarks = poseDetection.findPose(image,draw=True)

        window_x = image.shape[1]
        window_y = image.shape[0]
        if landmarks != None:
            right = [int(window_x*landmarks[15]["x"]),int(window_y*landmarks[15]["y"])]
            left = [int(window_x*landmarks[16]["x"]),int(window_y*landmarks[16]["y"])]
            cv2.circle(image, (right[0],right[1]),5,(255,0,0),cv2.FILLED)
            cv2.circle(image, (left[0],left[1]),5,(0,255,0),cv2.FILLED)

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()


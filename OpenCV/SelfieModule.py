import mediapipe as mp
import cv2
import numpy as np

class selfieDetector():
    def __init__(self,detectionCon=0.6):
        self.detectionCon = detectionCon
        self.selfie = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)

    def changeBackGround(self, img, bg_img):
        img.flags.writeable = False
        results = self.selfie.process(img)

        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        selfie_mask = np.stack((results.segmentation_mask,),axis=-1) > self.detectionCon

        bg_img = cv2.resize(bg_img,(img.shape[1],img.shape[0]))

        img = np.where(selfie_mask, img, bg_img)

        return img


if __name__=='__main__':
    import inspect
    selfieDetection = selfieDetector(detectionCon=0.5)
    mp_selfie_segmentation = mp.solutions.selfie_segmentation

    BG_COLOR = (192, 192, 192) # gray
    cap = cv2.VideoCapture(0)
    bg_image = cv2.imread('./images/2.jpg')
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        output_image = selfieDetection.changeBackGround(image, bg_image)

        cv2.imshow('MediaPipe Selfie Segmentation', output_image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()

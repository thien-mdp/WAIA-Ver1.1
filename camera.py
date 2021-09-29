import cv2
import test_train
import FaceMaskDetector
import os
import tensorflow as tf
from PIL import Image,ImageOps
import numpy as np
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
def name_to_color(name):
    # Take 3 first letters, tolower()
    # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
    color = [(ord(c.lower()) - 97) * 8 for c in name[:3]]
    return color
class MyVideoCapture:
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", 0)
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.video.isOpened():
            self.video.release()
    def getLabels(self):
        self.LABELS = []
        with open(os.path.join(CURRENT_DIR,"labels_facemask.txt"), 'r') as file:
            for x in file:
                self.LABELS.append(str(x).replace("\n", ""))
    def get_frame(self):
        if self.video.isOpened():
            faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            ret, frame = self.video.read()
            frame2 = frame
            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,

                scaleFactor=1.2,
                minNeighbors=5
                ,
                minSize=(20, 20)
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
    def cut_face(self,frame,top, right, bottom, left):
        x = left
        y = top
        w = right - x
        h = bottom - y

        frame = frame[y:y+h, x:x+w]
        return frame

    def TFpredictPilImg(self, pilImg):
        if (self.model == None):
            print("model is null")
            return None

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        image = ImageOps.fit(pilImg, self.size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        predictions = self.model.predict(data)

        result = np.argmax(predictions)
        return result, np.max(predictions)
    def PredictMat(self, mat):
        self.size = (224, 224)
        img = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, self.size)
        img_pil = Image.fromarray(img)

        result, acc = self.TFpredictPilImg(img_pil)
        return result, acc
    def get_frame_detect(self):
        self.getLabels()
        modelFile = os.path.join(CURRENT_DIR, "keras_model.h5")
        if (os.path.exists(modelFile)):
            self.model = tf.keras.models.load_model(modelFile)
        if self.video.isOpened():
            ret, frame = self.video.read()
            # result = faceMask.detect_mask_no_return_frame(frame2)
            predictions = test_train.predict_frame(frame, model_path="trained_knn_model.clf")
            list_name = []
            list_result = []
            if len(predictions) != 0:
                # for name, (top, right, bottom, left) in predictions:
                #     # print("- Found {} at ({}, {})".format(name, left, top))
                for name, (top, right, bottom, left) in predictions:
                    top_right = (right, top)
                    bottom_left = (left, bottom + 22)
                    bottom_right = (right, bottom)
                    a = left
                    b = bottom - top
                    top_left = (top, left)
                    try:
                        face = self.cut_face(frame, top, right, bottom, left)
                        predicted, acc = self.PredictMat(face)
                        result = self.LABELS[predicted]
                        cv2.putText(frame, str(result), top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, name_to_color(result), 1,
                                    cv2.FILLED)
                        list_name.append(name)
                        list_result.append(result)
                    except:
                        pass
                    cv2.rectangle(frame, top_right, bottom_left, (255, 0, 0), 3)
                    cv2.putText(frame, str(name), (left, bottom), cv2.FONT_HERSHEY_SIMPLEX, 1, name_to_color(name), 1,
                                cv2.FILLED)

            if ret:
                return (list_name,list_result,ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)

import cv2
import numpy as np

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

def detect_and_predict_mask(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (63.0, 0.0, 16.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()

    faces = []
    locs = []
    preds = []

    print("confidence : " + str(detections[0, 0, 0, 2]))

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        # if confidence > 0.1:
        print(detections[0,0,i,3:7])

        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        print(startX, startY, endX, endY)
        (startX, startY) = (max(0, startX), max(0, startY))
        if endX > w or endY > (h-1000):
            continue
        if endY - startY > (400):
            continue
        # (n_endX, n_endY) = (min(w - 1, endX), min(h - 1, endY))

        face = frame[startY:endY, startX:endX]
        if len(face) == 0 or face is None:
            continue
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (224, 224))
        face = img_to_array(face)
        face = preprocess_input(face)

        faces.append(face)
        locs.append((startX, startY, endX, endY))

        break


    if len(faces) > 0:

        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    return (locs, preds)
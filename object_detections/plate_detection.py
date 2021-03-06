import datetime
from ctypes import CDLL

import numpy as np
import time
import sys

import cv2
import os
from object_detections.service import Service
from ocr.plate_recognition import Ocr
sys.path.append(os.path.join(os.getcwd(), '/home/nilufer/Desktop/yolo/darknet/python'))
lib = CDLL(os.path.join(os.getcwd(), "libdarknet.so"), os.RTLD_GLOBAL)


class PlateDetection(Service):

    def save_image(self, image, extention, f_path):
        number = []

        for num in os.listdir(f_path):
            num = num.split("_")[1]
            number.append(num.split(".")[0])

        for i in range(0, len(number)):
            number[i] = int(number[i])

        number = sorted(number)
        size = len(number)

        if size == 0:
            next_number = 1
        else:
            next_number = int(number[size - 1]) + 1

        cv2.imwrite(f_path + "/object_%d" % next_number + extention, image)

    def get_model(self):
        np.random.seed(42)

        weightsPath = os.path.sep.join(["yolo-coco", "obj_60000.weights"])
        configPath = os.path.sep.join(["yolo-coco", "obj.cfg"])

        print("[INFO] loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        return net


    def start(self):

        net = self.get_model()

        labelsPath = os.path.sep.join(["yolo-coco", "obj.names"])
        LABELS = open(labelsPath).read().strip().split("\n")
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

        for file in os.listdir("cars"):

            file_name = file.split("_")[1]
            path = "cars/object_"+file_name
            image = cv2.imread(path)


            (H, W)= image.shape[:2]

            ln = net.getLayerNames()
            ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


            blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                         swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            layerOutputs = net.forward(ln)
            end = time.time()

            #print("[INFO] YOLO took {:.6f} seconds".format(end - start))

            boxes = []
            confidences = []
            classIDs = []

            for output in layerOutputs:
                for detection in output:

                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    if confidence > 0.5 :

                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")

                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)

            idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

            if len(idxs) > 0:
                for i in idxs.flatten():
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])

                    color = [int(c) for c in COLORS[classIDs[i]]]
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                    cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, color, 2)
                    if classIDs[i] != 0:
                        cropped_image = image[y:y + h, x:x + w]
                        height = cropped_image.shape[0]
                        width = cropped_image.shape[1]
                        if height != 0 and width != 0:
                            self.save_image(cropped_image, ".jpeg", "plates")
                        # cv2.imwrite("/home/nilufer/PycharmProjects/ewrwer/objects/object_%d" % i + ".jpeg", image2)

        ocr = Ocr()
        ocr.main()
    def Ocr(self):
        ocr = Ocr()
        ocr.main()
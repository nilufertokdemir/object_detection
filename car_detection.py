from ctypes import CDLL

import numpy as np
import time
import sys, os
import cv2
from service import Service

sys.path.append(os.path.join(os.getcwd(),'/home/nilufer/Desktop/yolo/darknet/python'))
lib = CDLL(os.path.join(os.getcwd(), "libdarknet.so"), os.RTLD_GLOBAL)

folder_path = "./cars"


class Car_image_detection(Service):

    def save_image(self,image, extention, f_path):
        numbers = []

        for file in os.listdir(f_path):
            numbers.append(file.split("_")[1])

        numbers_sorted = sorted(numbers)
        size = len(numbers)

        if size == 0:
            next_number = 1
        else:
            next_number = int(numbers_sorted[size - 1].split(".")[0]) + 1

        cv2.imwrite(f_path+"/object_%d" % next_number + extention, image)

    def get_model(self):
        np.random.seed(42)

        weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
        configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        return net


    def start(self):
        image = cv2.imread("./images/t32.jpeg")

        labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
        LABELS = open(labelsPath).read().strip().split("\n")

        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")

        net = self.get_model()


        (H, W) = image.shape[:2]

        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()

        print("[INFO] YOLO took {:.6f} seconds".format(end - start))

        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            for detection in output:

                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > 0.5:

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
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
                if classIDs[i] == 0:
                    print("Error!!")
                else:
                    cropped_image = image[y:y + h, x:x + w]
                    self.save_image(cropped_image,".jpeg",folder_path)
                    #cv2.imwrite("/home/nilufer/PycharmProjects/ewrwer/objects/object_%d" % i + ".jpeg", image2)





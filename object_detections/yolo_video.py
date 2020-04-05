import numpy as np
import argparse
import imutils
import time
import cv2
import os
from object_detections.service import Service


class Video_Detection(Service):

    def save_image(self, image, extention):
        number = []
        for num in os.listdir("cars"):
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
        print(next_number)
        cv2.imwrite("cars/object_%d" % next_number + extention, image)

    def get_model(self):
        np.random.seed(42)

        weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
        configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        return net

    def start(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--input",
                        default="videos/00005.mp4")
        ap.add_argument("-o", "--output",
                        default="output/overpass.avi")
        ap.add_argument("-y", "--yolo",
                        default="yolo-coco")
        ap.add_argument("-c", "--confidence", type=float, default=0.6,
                        help="minimum probability to filter weak detections")
        ap.add_argument("-t", "--threshold", type=float, default=0.4,
                        help="threshold when applyong non-maxima suppression")
        args = vars(ap.parse_args())

        labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
        LABELS = open(labelsPath).read().strip().split("\n")


        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                                   dtype="uint8")



        print("[INFO] loading YOLO from disk...")
        net = self.get_model()
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


        vs = cv2.VideoCapture(args["input"])
        writer = None
        (W, H) = (None, None)

        try:
            prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
                else cv2.CAP_PROP_FRAME_COUNT
            total = int(vs.get(prop))
            print("[INFO] {} total frames in video".format(total))


        except:
            print("[INFO] could not determine # of frames in video")
            print("[INFO] no approx. completion time can be provided")
            total = -1

        while True:

            (grabbed, frame) = vs.read()
            if not grabbed:
                break

            if W is None or H is None:
                (H, W) = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                         swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            layerOutputs = net.forward(ln)
            end = time.time()

            boxes = []
            confidences = []
            classIDs = []
            for output in layerOutputs:
                for detection in output:

                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]


                    if confidence > args["confidence"]:

                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")

                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
                                    args["threshold"])

            if len(idxs) > 0:

                for i in idxs.flatten():
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])

                    color = [int(c) for c in COLORS[classIDs[i]]]
                    #cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                    #cv2.putText(frame, text, (x, y - 5),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    if classIDs[i] != 0:
                        cropped_image = frame[y:y + h, x:x + w]
                        dimensions = cropped_image.shape

                        height = cropped_image.shape[0]
                        width = cropped_image.shape[1]

                        print(dimensions)
                        if int(height) != 0 | int(width) != 0:
                            self.save_image(cropped_image, ".jpeg")

            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(args["output"], fourcc, 30,
                                         (frame.shape[1], frame.shape[0]), True)

                if total > 0:
                    elap = (end - start)
                    print("[INFO] single frame took {:.4f} seconds".format(elap))
                    print("[INFO] estimated total time to finish: {:.4f}".format(
                        elap * total))

            writer.write(frame)

        print("[INFO] cleaning up...")
        writer.release()
        vs.release()
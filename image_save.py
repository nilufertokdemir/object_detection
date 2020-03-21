import os
import cv2
folder_path = "./cars"
folder_path2 = "./plates"


def save_image(image,extention,c):

    numbers = []

    if c == "c":
        for file in os.listdir(folder_path):
            numbers.append(file.split("_")[1])
    else :
        for file in os.listdir(folder_path2):
            numbers.append(file.split("_")[1])

    numbers_sorted = sorted(numbers)

    size = len(numbers)

    if size == 0:
        next_number = 1
    else :
        next_number = int(numbers_sorted[size - 1].split(".")[0]) + 1

    if c == "c":
        cv2.imwrite("./cars/object_%d" % next_number + extention, image)
    else :
        cv2.imwrite("./plates/object_%d" % next_number + extention, image)

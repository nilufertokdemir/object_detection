import os
import cv2


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
    print(next_number)
    cv2.imwrite(f_path + "/object_%d" % next_number + extention, image)
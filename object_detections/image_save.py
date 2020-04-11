from skimage.measure import compare_ssim
import argparse
import os
import cv2

j = 2
for file in os.listdir("cars"):

    # load the two input images
    imageA = cv2.imread("cars/object_1.jpeg")
    imageB = cv2.imread("cars/object_%d" % j+".jpeg")

    width = 250
    height = 200
    dim = (width, height)


    imageA = cv2.resize(imageA, dim, interpolation=cv2.INTER_AREA)# resize image
    imageB = cv2.resize(imageB, dim, interpolation=cv2.INTER_AREA)# resize image

    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    print("SSIM: {}".format(score) + "j: %d" % j)
    j += 1
'''
import skimage.io as sio
import skimage
import pytesseract
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
import cv2
image=sio.imread("/home/nilufer/Desktop/t1.png")

image=rgb2gray(image)
otsu=threshold_otsu(image)
imagebinari=image>otsu


#Tesseract Buradan itibaren kullanılıyor.
text=pytesseract.image_to_string(imagebinari,lang="tur",config="--psm 10")
print(text)
'''
'''
import cv2
import cv2
import pytesseract
from PIL import Image, ImageEnhance
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray

img = cv2.imread("/home/nilufer/Desktop/t5.png")

height, width, channels = img.shape
imgResized = cv2.resize(img, ( width*4, height*2))

image=rgb2gray(imgResized)
otsu=threshold_otsu(image)
imagebinari=image>otsu


im = Image.fromarray(imagebinari)
time = pytesseract.image_to_string(im,lang='tur', config ='-psm 11')
print(time)
'''


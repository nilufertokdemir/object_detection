import cv2

img = cv2.imread('TEST/dene4.jpeg', 0)

print('Original Dimensions : ', img.shape)

width = 300
height = 90
dim = (width, height)


resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)# resize image

print('Resized Dimensions : ', resized.shape)

# cv2.imshow("Resized image", resized)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imwrite('results/dene4.jpeg',resized)
# im = cv2.imread('resized.png')

#--------------------------------------------------------------------------------------

original_image = cv2.imread('results/dene4.jpeg') # Resim okuma işlemi.
cv2.imshow('cropped', original_image) # resmi gösterme.
cropped1= original_image[0:89, 42:106] # resmin istenen sırasıyla y ve x eksenlerini alma
cropped2= original_image[0:89, 106:191]
cropped3= original_image[0:89, 191:284]

images = [];

images.append(cropped1);
images.append(cropped2);
images.append(cropped3);

j=0;

for i in images:
    j+=1
    cv2.imwrite('demo_image/cropped'+str(j)+'.png',i)

cv2.imshow('kesilenResim',cropped3) # resmi gösterme.
cv2.waitKey() # gösterilen resmin kapanmasını engelleme.



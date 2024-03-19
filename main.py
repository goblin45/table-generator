import cv2 as cv
import numpy as np

image = cv.imread('sample.png', cv.IMREAD_GRAYSCALE)

cv.imshow('sample', image)
cv.waitKey(0)

imgArr = np.array(image)

row, col = imgArr.shape

for i in range(row):
    for j in range(col):
        print(imgArr[i][j], end=" ")
    print()
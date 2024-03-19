import cv2 as cv
import numpy as np

image = cv.imread('sample.png', cv.IMREAD_GRAYSCALE)

imgArr = np.array(image)

kernels = [
    # top left corner
    [
        [1, 1, 1],
        [1, 0, 0],
        [1, 0, 0]
    ],
    # top right corner
    [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],
    # bottom left corner
    [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ],
    # bottom right corner
    [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1]
    ],
    # center corner
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]
]

newImageArray = []

for i in range(len(kernels)):
    resImage = cv.filter2D(image, -1, np.array(kernels[i]))
    resImgArr = np.array(resImage)
    newImageArray.append(resImgArr)

cv.waitKey(0)

corners = set()

for i in range(len(newImageArray)):
    currImgArr = newImageArray[i]
    rows, cols = currImgArr.shape
    for row in range(rows): 
        for col in range(cols):
            if currImgArr[row][col] == 0:
                corners.add((col, row))

refinedCorners = set()
deletableCorners = set()

for corner1 in corners: 
    for corner2 in corners: 
        if corner1 == corner2:
            continue
        col1, row1 = corner1
        col2, row2 = corner2
        dist = np.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)
        if dist < 5: 
            deletableCorners.add(corner1)
            deletableCorners.add(corner2)
            avgRow = (row1 + row2) / 2
            avgCol = (col1 + col2) / 2
            newCorner = (avgCol, avgRow)
            refinedCorners.add(newCorner)
            print(corner1, "&", corner2, "changed into:", newCorner)

for corner in corners: 
    if corner not in deletableCorners:  
        refinedCorners.add(corner)
        
print("b")
print(refinedCorners)
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
    # [
    #     [0, 1, 0],
    #     [1, 1, 1],
    #     [0, 1, 0]
    # ]
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
                breakFlag = False
                for col1, row1 in corners:
                    dist = np.sqrt((row1 - row) ** 2 + (col1 - col) ** 2)
                    if dist < 4: 
                        avgCol = (col + col1) // 2
                        avgRow = (row + row1) // 2
                        corners.add((avgCol, avgRow))
                        corners.remove((col1, row1))
                        breakFlag = True
                        break
                if not breakFlag:
                    corners.add((col, row))

# print(sorted(corners, key= lambda x: x[0]))

filteredImgArr = []

for row in range(107):
    temp = []
    for col in range(180):
        if (col, row) in corners:
            temp.append(0)
        else:
            temp.append(255)
    filteredImgArr.append(temp)

filteredImage = np.uint8(filteredImgArr)
height, width = filteredImage.shape
resizedImage = cv.resize(filteredImage, (width * 2, height * 2))

cv.imshow('result', resizedImage)
cv.waitKey(0)
import cv2 as cv
import numpy as np
import csv
import pandas as pd
import easyocr

image = cv.imread("big-table.png", cv.IMREAD_GRAYSCALE)
reader = easyocr.Reader(["en"])

imgArr = np.array(image)

kernels = [
    # top left corner
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # top right corner
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    ],
    # bottom left corner
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    # bottom right corner
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
                    if dist < 15:
                        avgCol = (col + col1) // 2
                        avgRow = (row + row1) // 2
                        corners.add((avgCol, avgRow))
                        corners.remove((col1, row1))
                        breakFlag = True
                        break
                if not breakFlag:
                    corners.add((col, row))

corners = sorted(corners, key=lambda x: x[0])

cornersMat = []
diff = 15
prevCorner = corners[0]
tempCorners = []
for i in range(len(corners)):
    currX, currY = corners[i]
    if currX > prevCorner[0] + diff:
        cornersMat.append(tempCorners)
        tempCorners = [corners[i]]
        prevCorner = corners[i]
    else:
        tempCorners.append(corners[i])
if len(tempCorners) > 0:
    cornersMat.append(tempCorners)

for i in range(len(cornersMat)):
    cornersMat[i] = sorted(cornersMat[i], key=lambda x: x[1])

diagonal = -1
for row in range(len(cornersMat)):
    diagonal += 1
    for col in range(diagonal, len(cornersMat)):
        temp = cornersMat[row][col]
        cornersMat[row][col] = cornersMat[col][row]
        cornersMat[col][row] = temp

res = []
# subImageList = []
for i in range(len(cornersMat) - 1):
    temp = []
    for j in range(len(cornersMat[0]) - 1):
        corner1, corner2 = cornersMat[i][j], cornersMat[i][j + 1]
        corner3, corner4 = cornersMat[i + 1][j], cornersMat[i + 1][j + 1]
        x_min = min(corner1[0], corner2[0], corner3[0], corner4[0])
        x_max = max(corner1[0], corner2[0], corner3[0], corner4[0])
        y_min = min(corner1[1], corner2[1], corner3[1], corner4[1])
        y_max = max(corner1[1], corner2[1], corner3[1], corner4[1])
        subImgArr = imgArr[y_min - 2 : y_max + 2, x_min - 2 : x_max + 2]
        # subImageList.append(subImgArr)
        subImage = np.uint8(subImgArr)
        cv.imshow("SubIMG", subImage)
        cv.waitKey(0)
        extracted_text = reader.readtext(subImage)
        # if len(extracted_text) == 0:
        extra = 1
        while len(extracted_text) == 0:
            y_max += extra
            y_min -= extra
            x_max += extra
            x_min -= extra
            subImgArr = imgArr[y_min:y_max, x_min:x_max]
            subImage = np.uint8(subImgArr)
            extracted_text = reader.readtext(subImage)
        # else:
        string = ""
        for item in extracted_text:
            text = item[1]
            string += text
        temp.append(string)
    res.append(temp)

print(res)

resultCSV = "output_data.csv"


def save_to_csv(res, resultCSV):
    with open(resultCSV, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(res)


save_to_csv(res, resultCSV)
print(f"Data saved to {resultCSV}")

new_dataFrame = pd.read_csv("output_data.csv")
new_excel = pd.ExcelWriter("output_data.xlsx")
new_dataFrame.to_excel(new_excel, index=False)
new_excel._save()

with open("output_data.csv") as file_obj:
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        print(row)

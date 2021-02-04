"""
Vehicle-Detection-with-Scan-Data
COPYRIGHT © 2021 KIM DONGHEE. ALL RIGHTS RESERVED.
"""

import os
import glob
from PIL import Image
import cv2

imgName = "37"
scannerId = "2"
imgDir = "./data/img/" + imgName
cropDir = imgDir + "/" + imgName + "_" + scannerId
imgExt = ".png"

if not os.path.exists(imgDir):
    os.mkdir(imgDir)

img = cv2.imread(imgDir + "/" + imgName + "_" + scannerId + imgExt)
rows, cols = img.shape[0:2]  # size of img

divide = 7

border = rows//divide

top = border
bottom = border

imgBorder = cv2.copyMakeBorder(img, top, bottom, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])

if not os.path.exists(cropDir):
    os.mkdir(cropDir)

cv2.imwrite(cropDir + "/" + imgName + "_" + scannerId + "_border" + imgExt, imgBorder)


for_flip = cv2.imread(cropDir + "/" + imgName + "_" + scannerId + "_border" + imgExt)

vertical = cv2.flip(for_flip, 0)
ver_hor = cv2.flip(vertical, 1)

cv2.imwrite(cropDir + "/" + imgName + "_" + scannerId + "_border" + imgExt, ver_hor)

img_border_res = cv2.imread(cropDir + "/" + imgName + "_" + scannerId + "_border" + imgExt)
rows, cols = img_border_res.shape[0:2]  # size of img

movePixel = 10
h = rows
moveTimes = ((rows-border)//movePixel)+2

for i in range(moveTimes):
    img_border = Image.open(cropDir + "/" + imgName + "_" + scannerId + "_border" + imgExt)
    y = h - border
    w = img_border.size[0]

    croppedImage = img_border.crop((0, y, w, h))

    croppedImage.save(cropDir + "/" + imgName + "_" + scannerId + "_border_" + str(i) + imgExt)

    h = h - movePixel


img_array = []
for i in range(moveTimes):
    for filename in glob.glob(cropDir + "/" + imgName + "_" + scannerId + "_border_" + str(i) + imgExt):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(cropDir + "/" + imgName + "_" + scannerId + ".mp4", cv2.VideoWriter_fourcc(*'mp4v'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

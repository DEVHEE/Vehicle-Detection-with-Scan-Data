"""
Vehicle-Detection-with-Scan-Data
COPYRIGHT © 2021 KIM DONGHEE. ALL RIGHTS RESERVED.
"""

import os
from os.path import basename
from ctypes import *
from PIL import Image

DataNum = 381
imgPth = "./data/img/"
filename = "./data/raw/37.raw"


class Frame(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Len', c_int),  # length of ScannerNo~Data except Len itself
        ('ScannerNo', c_ushort),
        ('BitRefresh', c_ushort),
        ('SysTime', 16 * c_byte),
        ('StartAngle', c_int),
        ('DataLen', c_ushort),  # DataLen means the number of Data
        ('bDist0', c_bool),
        ('bDist1', c_bool),
        ('bRssi0', c_bool),
        ('bRssi1', c_bool),
        ('Data', DataNum * c_ushort),  # Data
    ]


for Sel_ScannerNo in range(10):
    FrameCnt, Sel_FrameCnt = 0, 0
    img = bytearray()
    fm = Frame()

    with open(filename, 'rb') as f:
        FileSize = os.path.getsize(filename)
        print("FileSize : ", FileSize)

        f.readinto(fm)
        FrameSize = 4 + fm.Len
        print("FrameSize : ", FrameSize)

        if DataNum == fm.DataLen:
            print("DataNum : ", DataNum)

        while FrameCnt < int(FileSize / FrameSize):
            if fm.ScannerNo == Sel_ScannerNo:
                for i in range(DataNum):
                    d = fm.Data[i]
                    if d > 0x3fff: d = 0x3fff  # modify to max 14bit
                    img.append((d >> 6) & 0xff)  # use only top 8bit (=distance resolution units are original * 64)
                Sel_FrameCnt += 1

            FrameCnt += 1
            f.readinto(fm)

        print("FrameCnt : ", FrameCnt)
        print("Sel_FrameCnt : ", Sel_FrameCnt)

    if Sel_FrameCnt:
        # convert bytearray "ba" to PIL Image, 'L' just means greyscale/lightness
        im = Image.frombuffer('L', (DataNum, Sel_FrameCnt), img, 'raw', 'L', 0, 1)
        imgName, imgExt = basename(filename).split(".")
        Outfilename = "/" + imgName + "_" + "%d" % Sel_ScannerNo + ".bmp"
        if not os.path.exists(imgPth):
            os.mkdir(imgPth)
        imgDir = "./data/img/" + imgName
        if not os.path.exists(imgDir):
            os.mkdir(imgDir)
        im.save(imgDir + Outfilename)

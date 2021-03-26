"""
Vehicle-Detection-with-Scan-Data
COPYRIGHT © 2021 KIM DONGHEE. ALL RIGHTS RESERVED.
"""

from PIL import Image
import numpy as np
import os

txtDir = "../data/raw/txt/"
tempDir = "../temp/"

f = open(txtDir + "37.txt", "r")
strings = f.read().splitlines()
search = "0000020000"

match_list = list()
for word in strings:
    if search in word:
        match_list.append(word)

# print(match_list)

# print(len(match_list))



for i in range(0, len(match_list)):
    line = match_list[i]
    # print(line)

    test_line = line[68:]
    # print(test_line)

    maxLen = 4  # the number of byte on once scan(line)
    chunks = [test_line[i:i+maxLen] for i in range(0, len(test_line), maxLen)]
    # print(chunks)

    res = []
    for i in range(2, int(len(test_line)), 4):
        info = test_line[i:i+2]
        res.append(info)
    # print(res)

    list = "".join(res)
    # print(list)

    if not os.path.isdir(tempDir):
        os.mkdir(tempDir)

    f = open(tempDir + 'test01.txt', 'a')  # open file
    print(list, file=f)  # save txt
    f.close()


with open(tempDir + 'test01.txt', 'r') as f:
    list_file = []
    for line in f:
        list_file.append(line.strip())

final_list = "".join(list_file)

# print(final_list)

final_arr = []
for i in range(0, int(len(final_list)), 2):
    info = final_list[i:i+2]
    final_arr.append(info)

# print(final_arr)
#
# print(len(final_list))
# print(len(final_arr))


hex = final_arr

decimal = [int(x, 16) for x in hex]
# print(test)

na = np.array(decimal, dtype=np.uint8)

# print(len(na))

# Make PIL Image from numpy array
im = Image.fromarray(na.reshape(len(match_list), int(len(hex)/len(match_list))))       # or im = Image.fromarray(na.reshape(8,4))

# Save
im.save('result2.png')
os.remove(tempDir + "test01.txt")
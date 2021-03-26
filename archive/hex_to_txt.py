"""
Vehicle-Detection-with-Scan-Data
COPYRIGHT © 2021 KIM DONGHEE. ALL RIGHTS RESERVED.
"""

import os
from glob import glob

# [START] CONVERT HEX TO TXT
hexDir = "../data/raw/hex/"
txtDir = "../data/raw/txt/"

ext = "hex"

if not os.path.isdir(hexDir):
    os.mkdir(hexDir)

if not os.path.isdir(txtDir):
    os.mkdir(txtDir)

# search .{ext} files on rawDir & set dir name
file_list_hex = glob(hexDir + "*." + ext)

for file_name in file_list_hex:
    basename = os.path.basename(file_name)
    name, ext = os.path.splitext(basename)

    f = open(txtDir + name + ".txt", "w")

    with open(hexDir + name + ext, 'rt', encoding='UTF8') as data:
        row_data = data.readlines()
        start_row = 0  # start row

    # write from row 0
    for i in range(start_row, len(row_data)-3):
        rows = row_data[i]
        if len(rows) < 17:  # ignore unused data
            continue
        else:
            f.write(rows[9:-3])  # write data by one line

    f.close()

    # read data from one line data txt file
    f = open(txtDir + name + ".txt", "r+")
    strings = f.readlines()
    text = strings[0]
    f.close()

    # split by chunks with the number of maxLen
    f = open(txtDir + name + ".txt", "w+")
    maxLen = 1592  # the number of byte on once scan(line)
    chunks = [text[i:i+maxLen] for i in range(0, len(text), maxLen)]
    for i in range(0, len(chunks)):
        line = chunks[i]
        f.write(line)  # rewrite in chunks
        f.write("\n")
    f.close()
# [END] CONVERT HEX TO TXT
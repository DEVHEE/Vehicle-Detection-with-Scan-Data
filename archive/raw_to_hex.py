"""
Vehicle-Detection-with-Scan-Data
COPYRIGHT © 2021 KIM DONGHEE. ALL RIGHTS RESERVED.
"""

import os
from glob import glob
import hexrec.records as hr

# [START] CONVERT RAW TO HEX
# set directory
rootDir = "../"
dataDir = "../data/"
rawDir = "../data/raw/"
hexDir = "../data/raw/hex/"

# set allowed extension
ext = "RAW"

if not os.path.isdir(hexDir):
    os.mkdir(hexDir)

# search .{ext} files
file_list = os.listdir(rawDir)
file_list_raw = [file for file in file_list if file.endswith(tuple(ext))]
print("Convert Queue: {}".format(file_list_raw))
print("Number of files: " + str(len(file_list_raw)) + "\n")

# search .{ext} files on rawDir & set dir name
file_list_raw = glob(rawDir + "*." + ext)

init_fileCount = 0

for file_name in file_list_raw:
    basename = os.path.basename(file_name)
    name, ext = os.path.splitext(basename)

    print("[Start {}/{}] Added to converting queue: {}".format(init_fileCount+1, len(file_list_raw), basename))
    hr.convert_file(file_name, hexDir + name + ".hex")  # convert file to hex
    print("[Complete {}/{}] Converting into HEX is finished: {} -> {}.hex".format(init_fileCount+1, len(file_list_raw), basename, name))
    init_fileCount += 1

print("Converting Completed!")
# [END] CONVERT RAW TO HEX
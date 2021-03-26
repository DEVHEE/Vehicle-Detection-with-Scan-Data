"""
Vehicle-Detection-with-Scan-Data
COPYRIGHT © 2021 KIM DONGHEE. ALL RIGHTS RESERVED.
"""

import matplotlib.pyplot as plt
import pandas as pd
import cv2
import random

cap = cv2.VideoCapture('test.mp4')
ret, frame = cap.read()
ratio = .5  # resize ratio
image = cv2.resize(frame, (0, 0), None, ratio, ratio)  # resize image

df = pd.read_csv('vehicle_data.csv')  # reads csv file and makes it a dataframe
rows, columns = df.shape  # shape of dataframe
print('Rows:',rows)
print('Columns:',columns)

fig1 = plt.figure(figsize=(10, 8))  # width and height of image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # plots first frame of video

for i in range(columns - 1):  # loops through all columns of dataframe, -1 since index is counted
    y = df.loc[df[str(i)].notnull(), str(i)].tolist()  # grabs not null data from column
    df2 = pd.DataFrame(y, columns=['xy'])  # create another dataframe with only one column

    # create another dataframe where it splits centroid x and y values into two columns
    df3 = pd.DataFrame(df2['xy'].str[1:-1].str.split(',', expand=True).astype(float))
    df3.columns = ['x', 'y']  # renames columns

    # plots series with random colors
    plt.plot(df3.x, df3.y, marker='x', color=[random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)],
             label='ID: ' + str(i))

# plot info
plt.title('Vehicle Centroids Data')
plt.xlabel('pos X')
plt.ylabel('pos Y')
plt.legend(bbox_to_anchor=(1, 1.2), fontsize='x-small')  # legend location and font
plt.show()
fig1.savefig('vehicle_data.png')  # saves image

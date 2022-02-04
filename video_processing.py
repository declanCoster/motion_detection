import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

vid = cv2.VideoCapture('cv_proj.mp4')       # open video stream
width = int(vid.get(3))
height = int(vid.get(4))
count = 0                                   # frame counter
background = []                             # the background photo
stdevs = []                                 # list for standard deviations
while vid.isOpened():                       # loop through frames
    count += 1                                  # interate counter
    if count % 50 == 0:                         # progress tracker
        print(count)
    ret, frame = vid.read()                     # get frames
    if frame is None:                           # break case
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):       # other break case
        break
    if count == 1:                              # set background as initial photo
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        continue
    diff_frame = cv2.absdiff(background, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    # get the difference between the background and the current frame.
    stdev = np.std(diff_frame)
    # calculate the standard deviation in the difference photo
    cv2.imwrite(os.path.join('diffs',f'{count}_diff.png'), diff_frame)
    # write difference image
    diff_thresh = cv2.threshold(diff_frame, 75, 255, cv2.THRESH_BINARY)[1]
    square = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    diff_thresh = cv2.erode(diff_thresh, square)
    diff_thresh = cv2.dilate(diff_thresh, square, iterations=2)
    # threshold, erode, and dilate to get the difference solid and strong
        # erode is needed to remove patchy noise.
    cv2.imwrite(os.path.join('threshold_diffs', f'{count}_thresh.png'), diff_thresh)
    stdevs.append(stdev)
    min_col = width
    max_col = 0
    min_row = height
    max_row = 0
    object_noticed = False
    for row in range(height):
        for col in range(width):
            if diff_thresh[row, col]:
                if max_row < row:
                    max_row = row
                elif min_row > row:
                    min_row = row
                if max_col < col:
                    max_col = col
                elif min_col > col:
                    min_col = col
                object_noticed = True

    if object_noticed and (max_row - min_row) + (max_col - min_col) >= 50:
        # the last part of the if is to try and reduce small rectangles that won't be useful
        # this is sort of another noise reduction step.git 
        cv2.rectangle(frame, (min_col, min_row), (max_col, max_row), (0,0,255), 3)
    cv2.imwrite(os.path.join('selected', f'{count}_sel.png'), frame)

vid.release()
fig, ax = plt.subplots()
ax.plot(stdevs)
ax.set_title('Stdev over Frames')
ax.set_xlabel('Frames')
ax.set_ylabel('Stdev')
fig.savefig('stdev_plot.png')


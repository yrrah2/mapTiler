import cv2
import os
from pathlib import Path
from math import floor

def filestr(depth, x, y):
    return "map/" + str(depth) + "/" + str(x) + "/" + str(y) + ".png"

def refactorUp(depth, x, y):
    print("Trying to open: " + str(depth) + "/" + str(x) + "/" + str(y))
    if depth > 0:
        # Load the image, and find the larger image to push it into
        smaller = cv2.imread(filestr(depth,   x,          y          ))
        larger  = cv2.imread(filestr(depth-1, floor(x/2), floor(y/2) ))

        # Resize the image to fit into the larger one
        resized = cv2.resize(smaller, None, fx= 0.5, fy= 0.5, interpolation= cv2.INTER_LINEAR)

        #Calculate the offset to overlay with
        height, width, channels = resized.shape
        yo, xo = 1,1
        if y % 2 == 0:
            yo=0
        if x % 2 == 0:
            xo=0
        y_offset = yo*height
        x_offset = xo*width

        cv2.imshow("Before", larger)

        # Overlay the images
        larger[y_offset:y_offset+resized.shape[0], x_offset:x_offset+resized.shape[1]] = resized

        # Show the finished product
        cv2.imshow("After", larger)
        cv2.imwrite(filestr(depth-1, floor(x/2), floor(y/2) ), larger)
        refactorUp(depth-1, floor(x/2), floor(y/2))

def refactorDown(depth, x, y, extent):
    print("Trying to open: " + str(depth) + "/" + str(x) + "/" + str(y))
    if depth > 0:
        # Load the image, and find the larger image to push it into
        smaller = cv2.imread(filestr(depth,   x,          y          ))
        larger  = cv2.imread(filestr(depth-1, floor(x/2), floor(y/2) ))

        # Resize the image to fit into the larger one
        resized = cv2.resize(smaller, None, fx= 0.5, fy= 0.5, interpolation= cv2.INTER_LINEAR)

        #Calculate the offset to overlay with
        height, width, channels = resized.shape
        yo, xo = 1,1
        if y % 2 == 0:
            yo=0
        if x % 2 == 0:
            xo=0
        y_offset = yo*height
        x_offset = xo*width

        cv2.imshow("Before", larger)

        # Overlay the images
        larger[y_offset:y_offset+resized.shape[0], x_offset:x_offset+resized.shape[1]] = resized

        # Show the finished product
        cv2.imshow("After", larger)
        cv2.imwrite(filestr(depth-1, floor(x/2), floor(y/2) ), larger)
        refactorUp(depth-1, floor(x/2), floor(y/2))
	
refactorUp(2, 2, 1)

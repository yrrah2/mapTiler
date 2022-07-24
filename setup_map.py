import cv2
import os
from pathlib import Path
from math import floor

def mkfolder(path):
    if not(os.path.exists(path) and os.path.isdir(path)):
        os.mkdir(path)

def filestr(depth, x, y):
    return "map/"+str(depth)+"/"+str(x)+"/"+str(y)+".png"

def divide(image):
    # cv2.imread() -> takes an image as an input
    h, w, channels = image.shape

    half_width  = w//2
    half_height = h//2

    quarters = [[
            image[:half_height, :half_width],
            image[half_height:, :half_width]
        ],[
            image[:half_height, half_width:],
            image[half_height:, half_width:]
                ]]
    
    quarters_resized = [[],[]]
    for i in 0,1:
        for j in 0,1:
            quarters_resized[i].append(cv2.resize(quarters[i][j], (0, 0), fx=2, fy=2))
    return quarters_resized

def setup_main(mapfile, totalDepth):
    basemap = cv2.imread(mapfile)

    # Make the folders
    mkfolder("map")
    for depth in range(totalDepth):
        mkfolder("map/"+str(depth))
        for i in range(2**depth):
            mkfolder("map/"+str(depth)+"/"+str(i))

    # Place the files
    for depth in range(totalDepth-1):
        for i in range(2**depth):
            for j in range(2**depth):
                print(depth, i, j)
                x = cv2.imread(filestr(depth,i,j))
                q = divide(x)
                for k in range(2):
                    for l in range(2):
                        cv2.imwrite(filestr(depth+1, 2*i+k, 2*j+l), q[k][l])

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
    if extent > 0:
        img = cv2.imread(filestr(depth, x, y))
        q = divide(img)
        for i in range(2):
            for j in range(2):
                print("Updating: {}/{}/{}.".format(depth+1, 2*x+i, 2*y+j))
                cv2.imwrite(filestr(depth+1, 2*x+i, 2*y+j), q[i][j])
                
        for i in range(2):
            for j in range(2):
                refactorDown(depth+1, 2*x+i, 2*y+j, extent-1)

##        # Place the files
##        for depth in range(totalDepth-1):
##            for i in range(2**depth):
##                for j in range(2**depth):
##                    print(depth, i, j)
##                    x = cv2.imread(filestr(depth,i,j))
##                    q = divide(x)
##                    for k in range(2):
##                        for l in range(2):
##                            cv2.imwrite(filestr(depth+1, 2*i+k, 2*j+l), q[k][l])
	


#setup_main("basemap.png", 6)
refactorUp(2, 2, 2)
refactorDown(2, 2, 2, 3)

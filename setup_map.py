import cv2
import os
from pathlib import Path
from math import floor

def mkfolder(path):
    if not(os.path.exists(path) and os.path.isdir(path)):
        os.mkdir(path)

def filestr(depth, x, y, filetype="none"):
    if filetype=="map":
        path_string = "map/"+str(depth)+"/"+str(x)+"/"+str(y)+"_map.png"
    else:
        path_string = "map/"+str(depth)+"/"+str(x)+"/"+str(y)+".png"
    return path_string

def divide(image):
    # cv2.imread() -> takes an image as an input
    h, w, channels = image.shape

    half_width  = 512 #w//2
    half_height = 512 #h//2

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
            resized = cv2.resize(quarters[i][j], (0, 0), fx=2, fy=2)
            thresh = 127
            im_bw = cv2.threshold(resized, thresh, 255, cv2.THRESH_BINARY)[1]
            quarters_resized[i].append(im_bw)
    return quarters_resized

def convert_masks(totalDepth):
    land = cv2.imread("land.png")
    sea = cv2.imread("sea.png")

    # Place the files
    for depth in range(totalDepth):
        for i in range(2**depth):
            for j in range(2**depth):
                print("Converting:  {}/{}/{}.".format(depth, i, j))
                mask = cv2.imread(filestr(depth,i,j), 0)
                mask_inverse = cv2.bitwise_not(mask)

                land_part = cv2.bitwise_and(land,land,mask = mask_inverse)
                sea_part = cv2.bitwise_and(sea,sea,mask = mask)
                
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                land_and_sea = cv2.add(land_part, sea_part)
                cv2.drawContours(land_and_sea, contours, -1, (26, 32, 40), 1)

                cv2.imwrite(filestr(depth, i, j, "map"), land_and_sea)


def setup_main(mapfile, totalDepth):
    basemap = cv2.imread(mapfile)


    # Make the folders
    mkfolder("map")
    for depth in range(totalDepth):
        mkfolder("map/"+str(depth))
        for i in range(2**depth):
            mkfolder("map/"+str(depth)+"/"+str(i))

    print("Making masks\n")

    # Place the files
    for depth in range(totalDepth-1):
        for i in range(2**depth):
            for j in range(2**depth):
                print("Opening: {}/{}/{}.".format(depth, i, j))
                x = cv2.imread(filestr(depth,i,j))
                q = divide(x)
                for k in range(2):
                    for l in range(2):
                        print("Updating: {}/{}/{}.".format(depth+1, 2*i+k, 2*j+l))
                        cv2.imwrite(filestr(depth+1, 2*i+k, 2*j+l), q[k][l])

    print("Converting to maps\n")
    convert_masks(totalDepth)


def refactorUp(depth, x, y):
    print("Opening: {}/{}/{}.".format(depth, x, y))
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

        # Overlay the images
        larger[y_offset:y_offset+resized.shape[0], x_offset:x_offset+resized.shape[1]] = resized

        # Show the finished product
        print("Updating: {}/{}/{}.".format(depth-1, floor(x/2), floor(y/2)))
        cv2.imwrite(filestr(depth-1, floor(x/2), floor(y/2) ), larger)
        refactorUp(depth-1, floor(x/2), floor(y/2))

def refactorDown(depth, x, y, extent):
    if extent > 0:
        print("Opening: {}/{}/{}.".format(depth, x, y))
        img = cv2.imread(filestr(depth, x, y))
        q = divide(img)
        for i in range(2):
            for j in range(2):
                print("Updating: {}/{}/{}.".format(depth+1, 2*x+i, 2*y+j))
                cv2.imwrite(filestr(depth+1, 2*x+i, 2*y+j), q[i][j])
                
        for i in range(2):
            for j in range(2):
                refactorDown(depth+1, 2*x+i, 2*y+j, extent-1)

convert_masks(4)
#setup_main("world.png", 4)
#refactorDown(1,0,1,2)

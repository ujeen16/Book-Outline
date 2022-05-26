import cv2
import numpy as np
from math import sqrt

BLACK = (0, 0, 0)


# conects 4 points and draws the shape. I am using this to draw a rectangle
def connectTheDots(image, xy1, xy2, xy3, xy4):
    # need integers to work with pixels
    xy1 = [int(x) for x in xy1]
    xy2 = [int(x) for x in xy2]
    xy3 = [int(x) for x in xy3]
    xy4 = [int(x) for x in xy4]
    # draw lines to connect points. rectange might work but lines allow more flexability
    # incase we want to allow a bit less of a rectangular shape
    cv2.line(img, xy1, xy2, BLACK, 6)
    cv2.line(img, xy3, xy4, BLACK, 6)
    cv2.line(img, xy1, xy3, BLACK, 6)
    cv2.line(img, xy2, xy4, BLACK, 6)


img = cv2.imread("book1.jpg", 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("the book", img)
cv2.imshow("gray book", gray)

# find the corners. problem found 19 other corners. seems difficult to find it such that only
# the found indicated corners appear
gray = cv2.dilate(gray, None)
corners = cv2.goodFeaturesToTrack(gray, maxCorners=23, qualityLevel=0.1, minDistance=10)

# this displays all the corners
for item in corners:
    x, y = item[0]
    x = int(x)
    y = int(y)
    cv2.circle(img, (x, y), 6, (150, 150, 2), -1)

# loop through every iteration of points possible. ie) 23*22*21*20. and create vectors with them
# note two points can't be the same
# we check and only keep vectors which are close to equal
# finally we search for a rectangle. so  we get a third vector and check if the dot product is close to zero(see attached img)
# this indicates a right angle or close to it meaning a rectangle. we find the same rectangle twice
# count and counter don't make any difference in the code
count = 0
counter = 0
for i in range(len(corners)):
    currentXY = corners[i][0]
    for j in range(len(corners)):
        if j == i:
            continue
        otherXY = corners[j][0]
        vec1 = [otherXY[0]-currentXY[0], otherXY[1]-currentXY[1]]
        for k in range(len(corners)):
            if k == (i or j):
                continue
            nextXY = corners[k][0]
            for l in range(len(corners)):
                if l == (i or j or k):
                    continue
                finalXY = corners[l][0]
                vec2 = [finalXY[0]-nextXY[0], finalXY[1]-nextXY[1]]
                vec3 = [currentXY[0]-nextXY[0], currentXY[1]-nextXY[1]]

                # check if the vectors are close to equal
                if (vec1[0]-3) <= vec2[0] <= (vec1[0]+3) and (vec1[1]-5) <= vec2[1] <= (vec1[1]+3):
                    count += 1
                    # we have 46 matching vectors. only one will be very close to a right angle so we will
                    # take the dot product of two vectors to find a right angle meaning that we will have a
                    # rectangle. if the dot is close enough to zero it is right angle
                    dotProduct = (vec1[0] * vec3[0]) + (vec1[1] * vec3[1])
                    if -10 <= dotProduct <= 10:
                        counter += 1
                        connectTheDots(img, nextXY, finalXY, currentXY, otherXY)

print("matching vector count:", count)
# found two of the same because the solution is brute force
print("rectangle count", counter)

cv2.imshow("final", img)

cv2.waitKey(0)

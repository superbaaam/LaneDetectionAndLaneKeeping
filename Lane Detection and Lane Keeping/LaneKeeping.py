import numpy as np
import cv2
from easygopigo3 import EasyGoPiGo3
#import random
gpg = EasyGoPiGo3()
gpg.set_speed(50)

cap = cv2.VideoCapture(-1)

mtx = np.float32([[495.37640381, 0, 327.21967209],
                  [0, 500.3762207, 244.67909188],
                  [0, 0, 1]])

dist = np.float32(
    [[0.14067485, -0.18943851, -0.00527697,  0.00327764, -0.22035553]])


def undistort_image(image):
    return cv2.undistort(image, mtx, dist, None, mtx)


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 5)
    return line_image


def perspectiveWarp(inpImage):
    # Get image size
    inpWidth, inpHeight = (inpImage.shape[1], inpImage.shape[0])

    # TOPLEFT , TOPRIGHT, BOTTOMLEFT, BOTTOMRIGHT
    # cropped X,Y
    # sPt_A = [225,0]
    # sPt_B = [433,0]
    # sPt_C = [0, inpHeight]
    # sPt_D = [620, inpHeight]

    # With Border X,Y
    sPt_A = [205, 0]
    sPt_B = [439, 0]
    sPt_C = [0, 205]
    sPt_D = [596, 205]

    src = np.float32([sPt_A, sPt_B, sPt_C, sPt_D])
    dst = np.float32([(160, 0), (480, 0), (160, 640), (480, 640)])

    matrix = cv2.getPerspectiveTransform(src, dst)
    # Inverse matrix to unwarp the image for final window
    minv = cv2.getPerspectiveTransform(dst, src)
    birdseye = cv2.warpPerspective(inpImage, matrix, (640, 640))

    return birdseye, minv

# def getHistogram(img, flag):


#     # if region == 1:
#     histValues = np.sum(img, axis=0)
#     # else:
#     #     histValues = np.sum(img[img.shape[0]:, :], axis=0)
#     #print(histValues)

#     maxValue = np.max(histValues)
#     #print("maxValue: ", maxValue)
#     minValue = 0.15 * maxValue
#     # # print("maxValue: " + str(maxValue))
#     # # print("minPer: " + str(minPer))
#     # # print("minValue: " + str(minValue))

#     # Offset durch den Unterschied der Dicke von Mittelstreifen zur Außenmarkierung
#     laneOffset = 30
#     flagFactor = 0.2
#     indexArray = np.where(histValues >= minValue)
#     if flag:    # Nur eine Fahrspur erkannt
#         maxfind = np.where(histValues == maxValue)
#         #print("maxfind: ",maxfind)
#         #print("maxfind[0][0]: ",maxfind[0][0])
#         if maxfind[0][0] > 302:
#             #print("Correction to left")
#             dif = maxfind[0][0] - 302
#             basePoint = int(int(np.average(indexArray)) + laneOffset - (flagFactor * dif))
#         else:
#             #print("Correction to right")
#             dif = 302 - maxfind[0][0]
#             basePoint = int(int(np.average(indexArray)) + laneOffset - (flagFactor * dif))

#     else:
#         basePoint = int(np.average(indexArray)) + laneOffset

#     imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
#     for x, intensity in enumerate(histValues):
#         cv2.line(imgHist, (x, img.shape[0]), (x, img.shape[0]-intensity//255), (255, 0, 255), 1)
#         cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
#     #return basePoint
#     return basePoint, imgHist

# def steering_calc(list, center, heightdif, height):
#     angles = []
#     trajectory = []

#     for index in range(len(list)): # 0..3
#     # for index in range(2):
#         # Calc Alpha
#         aktHeight = (heightdif*index) + (heightdif/2)
#         alpharad = np.arctan((list[index]-center)/ (aktHeight))
#         #print("Alpha: ",alpharad, " list: ", list[index], " center: ", center)
#         #print("index: ",index, " aktHeight: ", aktHeight)
#         alphadeg = np.rad2deg(alpharad)
#         angles.append(alphadeg)

#         # Append Trajectory List
#         # Variant 1
#         if index == 0:
#             trajectory.append([(center,height),(list[index],int(height-(heightdif/2)))])
#         else:
#             trajectory.append([(list[index-1],int(height-(heightdif/2 + (index-1)*heightdif))) , (list[index], int(height-heightdif/2 - (index)*heightdif))])

#     # Variant 2
#     #trajectory.append([(center,height),(list[len(list)-1], int(height-((len(list)-1)*heightdif)))])
#     #print(trajectory)
#     steering_avg = sum(angles) / len(angles)
#     return steering_avg , trajectory

def trajectoryCalc(list, center, heightdif, height):
    targetPoints = []
    for index in range(len(list)-2):  # 0..2
        targetPoints.append(list[index+1])
        # print(list[index+1])
    # print(targetPoints)
    targetX = int(sum(targetPoints) / len(targetPoints))
    #targetY = int(height/2)
    targetVector = [(center, height), (targetX, 0)]
    #print("target: ",target)
    return targetVector, targetX  # [(x,y) , (x,y)]


def trajectoryimg(img, target):
    #[(276, 280), (280, 200)]
    offset = 320
    birdeyeOffset = 20
    cv2.line(img, (target[0][0]+birdeyeOffset, target[0][1]+offset),
             (target[1][0], target[1][1]+offset), (255, 255, 255), 4)
    return img


def getLaneinfo(img, height):
    # cv2.imshow("crop",img)
    testHeight, testWidth = img.shape[:2]
    # print("Height: ", testHeight, "Width: ", testWidth) # 80 x 640
    Left = []
    Right = []

    for row in range(0, testHeight, 10):
        # print(gray_img[10:10+1, 0:320])
        leftLanefound = False
        rightLanefound = False

        col = 321
        while not leftLanefound and col > 0:
            if img[row, col] > 180:
                Left.append((row, col))
                leftLanefound = True
                break
            col = col - 1

        col = 321
        while not rightLanefound and col < 640:
            if img[row, col] > 180:
                Right.append((row, col))
                rightLanefound = True
                break
            col = col + 1

        if not leftLanefound and rightLanefound:  # Links nicht gefunden, Rechts schon
            avgRightX, avgRightY = int(sum(i[1] for i in Right) / len(Right)), int(sum(i[0]
                                                                                       for i in Right) / len(Right))
            avgLeftY = avgRightY
            if avgRightX > 260:
                avgLeftX = avgRightX - 260  # Fahrspurbreite in px
            else:
                avgLeftX = 0
        elif leftLanefound and not rightLanefound:  # Links gefunden, aber Rechts nicht
            avgLeftX, avgLeftY = int(sum(i[1] for i in Left) / len(Left)), int(sum(i[0]
                                                                                   for i in Left) / len(Left))
            avgRightY = avgLeftY
            if avgLeftX < 380:
                avgRightX = avgLeftX + 260  # Fahrspurbreite in px
            else:
                avgRightX = 640
        elif not leftLanefound and not rightLanefound:  # Keine Spur gefunden!
            avgLeftX, avgLeftY = 190, 45
            avgRightX, avgRightY = 445, 40
            #print("no lane")
        else:
            avgLeftX, avgLeftY = int(sum(i[1] for i in Left) /
                                     len(Left)), int(sum(i[0] for i in Left) / len(Left))
            avgRightX, avgRightY = int(sum(i[1] for i in Right) / len(Right)), int(sum(i[0]
                                                                                       for i in Right) / len(Right))

    point = (int((avgLeftX+avgRightX) / 2), int((avgLeftY + avgRightY) / 2))
    #cv2.circle(img, (point[0],point[1]), 10, (255, 255, 255), cv2.FILLED)
    #print("avgLeftX: ", avgLeftX, "avgLeftY: ", avgLeftY, "avgRightX: ", avgRightX, "avgRightY: ", avgRightY)
    #print("point: ",point)
    return point[0]


def regionCrop(img, count):

    # Init List of MIddlepoints, Crop birdview image to half of height
    middlePoints = []

    regionHeight, regionWidth = img.shape[:2]   # 640 x 640
    #print("regionHeight: ",regionHeight, "regionWidth: ", regionWidth)
    crop_img = img[int(regionHeight/2): regionHeight, 0: regionWidth]
    cropHeight, cropWidth = crop_img.shape[:2]  # 320 x 640
    #print("cropHeight: ",cropHeight, "cropWidth: ", cropWidth)
    #cv2.imshow("crop_img", crop_img)
    countHeight = round(cropHeight / count)
    #print("countHeight: ", countHeight)

    for index in range(count):
        crop_bird = crop_img[int(cropHeight-(index+1)*countHeight)
                                 : int(cropHeight-index*countHeight), 0: cropWidth]
        cv2.imshow("crop", crop_bird)
        middlePoint = getLaneinfo(crop_bird, countHeight)
        #print("middlePoint: ", middlePoint)
        middlePoints.append(middlePoint)
        #cv2.imshow("crop", crop_bird)

    return middlePoints, countHeight, cropHeight


def detect_lanes_img(img):
    # Init Paramters
    height, width = img.shape[:2]   # 480 x 640

    # Apply Image Correction
    image_undistort = undistort_image(img)

    # Get ROI + Cutting Borders caused by undistort
    roi_img = image_undistort[int(height * 0.4):height-5, 0: width-10]
    roi_height, roi_width = roi_img.shape[:2]  # 283 x 630
    #print(roi_height, " ", roi_width)

    # Get Lane Information
    # Convert to grayimage
    gray_img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)

    # Apply gaussian filter
    blur_img = cv2.GaussianBlur(gray_img, (3, 3), 0)
    #blur_img = cv2.GaussianBlur(gray_img,(5, 5), 0)

    # Apply Canny edge transform
    canny_img = cv2.Canny(blur_img, 100, 130)
    #canny_img = cv2.Canny(blur_img, 150, 210)

    # Apply Threshold Function
    _, thresh_img = cv2.threshold(gray_img, 64, 255, cv2.THRESH_BINARY_INV)

    # Combine Canny and Threshold for better result
    combo_image = cv2.addWeighted(thresh_img, 1, canny_img, 1, 1)

    # Apply Hough Transformation
    lines = cv2.HoughLinesP(canny_img, 2, np.pi/180, 10,
                            np.array([]), minLineLength=100, maxLineGap=60)

    line_image = display_lines(roi_img, lines)
    lane_image = cv2.addWeighted(roi_img, 1, line_image, 1, 1)

    # Apply Perspective Warping
    #birdView, minverse = perspectiveWarp(roi_img)
    birdView, minverse = perspectiveWarp(combo_image)
    #birdView, minverse = perspectiveWarp(lane_image)

    # Get Middle Information
    # Middle Marker
    realCenter = 302    # wahre Mitte des Fahrzeugs
    cv2.line(lane_image, (realCenter, roi_height),
             (realCenter, roi_height-80), (0, 255, 0), 2)

    # Crop Image into X Pieces
    nIntervalls = 4
    middlePoints, IntervallHeight, cropHeight = regionCrop(
        birdView, nIntervalls)
    #print("middlePoints: ", middlePoints, "IntervallHeight: ", IntervallHeight)
    target, targetX = trajectoryCalc(
        middlePoints, realCenter, IntervallHeight, cropHeight)

    birdView2, minverse = perspectiveWarp(roi_img)
    traject_bird = trajectoryimg(birdView2, target)
    #traject_image = cv2.warpPerspective(traject_bird, minverse, (630, 200))

    # rand = random.randrange(0, 101, 2)
    # if cv2.waitKey(1) == ord("w"):
    #     cv2.imwrite(f"Screenshot{rand}.jpg", birdView2)

    # OUTPUT
    #cv2.imshow("traject_bird", traject_bird)
    #cv2.imshow("traject_image", traject_image)
    cv2.imshow("birdView2", birdView2)
    # cv2.imshow("Histogram",imgHist)
    #cv2.imshow("birdView", birdView)
    cv2.imshow("lane_image", lane_image)
    # cv2.imshow("Histogram",imgHist)
    #cv2.imshow("roi_img", roi_img)
    #cv2.imshow("cannyroi", canny_img)
    #cv2.imshow("threshroi", thresh_img)
    #cv2.imshow("combo_image", combo_image)

    return realCenter, targetX


if __name__ == '__main__':
    while (cap.isOpened()):

        # Get Data
        ret, frame = cap.read()

        # Get Detect Lane
        #result = detect_lanes_img(frame)
        Ist, Soll = detect_lanes_img(frame)
        #print("Ist: ", Ist, "Soll: ", Soll)

        Faktor = 0.5

        SollIstDif = Soll - Ist

        left, right = 100, 100

        if (SollIstDif < 0):      # <0:Linkskurve
            left = left + (SollIstDif * Faktor)
            gpg.steer(left, right)
            # print("LINKS")
            #print("left: ",left, "right: ", right)

        else:                   # >0: Rechtskurve
            right = right - (SollIstDif * Faktor)
            gpg.steer(left, right)
            # print("RECHTS")
            #print("left: ",left, "right: ", right)

        # Output
        #cv2.imshow('result', result)
        # out.write(frame)

        if cv2.waitKey(1) == ord('q'):
            gpg.stop()
            break

    cap.release()
    cv2.destroyAllWindows()

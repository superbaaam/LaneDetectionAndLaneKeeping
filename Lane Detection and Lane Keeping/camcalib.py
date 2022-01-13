# https://github.com/tizianofiorenzani/how_do_drones_work/blob/master/opencv/cameracalib.py
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration

import numpy as np
import cv2
import glob

# Parameter
nRows = 9
nCols = 6

# termination criteria
iterations = 30
epsilon = 0.001
criteria = (cv2.TERM_CRITERIA_EPS +
            cv2.TERM_CRITERIA_MAX_ITER, iterations, epsilon)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((nCols * nRows, 3), np.float32)  # Test Reihenfolge!!
objp[:, :2] = np.mgrid[0:nRows, 0:nCols].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.


# path="/home/pi/Desktop/Images/CalibrationImages/"

path_2 = "/home/pi/Desktop/Images/Undistort/"  # Undistorted Image

images = glob.glob("/home/pi/Desktop/Images/CalibrationImages/*.jpg")
#images = glob.glob(path + "cali_img_*.jpg")

index = 0
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (nRows, nCols), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        # corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)     #RMS Error: 0.761
        corners2 = cv2.cornerSubPix(
            gray, corners, (5, 5), (-1, -1), criteria)  # RMS Error: 0.756
        imgpoints.append(corners2)

        # Draw and display the corners
        # cv2.drawChessboardCorners(img, (nRows,nCols), corners2,ret)  #Calibration pattern
        # cv2.imshow('img',img)
        #cv2.imwrite(f"{path_2}_{index}.jpg", img)
        #index = index + 1
        # cv2.waitKey(500)

cv2.destroyAllWindows()

# Calibration Process and output
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

#print("RMS error: ")
print("Projection error: ")
print(ret)
print("Calibration Matrix: ")
print(mtx)
print("Disortion: ", dist)

""" OUTPUT
RMS error: 
0.7560896986500854
Calibration Matrix: 
[[491.42696616   0.         324.94234698]
 [  0.         491.05136316 247.04393601]
 [  0.           0.           1.        ]]
Distortion:  [[ 0.14253517 -0.2042386  -0.00530606  0.0032225  -0.1927077 ]]

"""

# Undistort Image
img = cv2.imread(f"{path_2}cali_img_7.jpg")
img = cv2.imread("/home/pi/Desktop/Images/Undistort/cali_img_7.jpg")
cv2.imshow('img', img)
cv2.waitKey(0)

h,  w = img.shape[:2]
alpha = 0
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
    mtx, dist, (w, h), alpha, (w, h))

print("New Calibration Matrix: ")
print(newcameramtx)

# undistort
mapx, mapy = cv2.initUndistortRectifyMap(
    mtx, dist, None, newcameramtx, (w, h), 5)
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv2.imshow("Undistorted Image", dst)
cv2.imwrite('calibresult.png', dst)


""" OUTPUT
alpha = 1
New Calibration Matrix: 
[[361.38467407   0.         381.53738842]
 [  0.         325.50531006 256.96436262]
 [  0.           0.           1.        ]]

alpha = 0
New Calibration Matrix: 
[[495.37640381   0.         327.21967209]
 [  0.         500.3762207  244.67909188]
 [  0.           0.           1.        ]]


"""

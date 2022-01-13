# LaneDetectionAndLaneKeeping

This project is part of my bachelor's thesis.
The goal is to get a gopigo car to detect lanes provided by the raspberry pi camera v2. Return an information about the direction of the lane and keep the lane with a p-controller. Additionally, I implemented an obstacle detection with a haar cascade for cars.

## Pipeline

<img src="https://user-images.githubusercontent.com/97686850/149362141-2ca207eb-6623-4bba-89dd-0e2a0be186b6.png" alt="Pipeline" width="450"/> <img src="https://user-images.githubusercontent.com/97686850/149362150-7e40e167-68ca-4e93-a7d1-43827c63c622.png" alt="Pipeline" width="500"/>

**The workthrough is the following:**

A possibly distorted input image is provided by the raspberry pi camera. With the file camcalib.py the input image is getting undistorted 

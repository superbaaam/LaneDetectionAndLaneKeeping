# LaneDetectionAndLaneKeeping

This project is part of my bachelor's thesis.
The goal is to get a gopigo car to detect lanes provided by the raspberry pi camera v2. Return an information about the direction of the lane and keep the lane with a p-controller. Additionally, I implemented an obstacle detection with a haar cascade for cars.

## Pipeline

<img src="https://user-images.githubusercontent.com/97686850/149362141-2ca207eb-6623-4bba-89dd-0e2a0be186b6.png" alt="Pipeline" width="450"/> <img src="https://user-images.githubusercontent.com/97686850/149362150-7e40e167-68ca-4e93-a7d1-43827c63c622.png" alt="Pipeline" width="500"/>

**The workthrough of the lane detection and lane keeping is the following:**

- A possibly distorted input image is provided by the raspberry pi camera. With the file camcalib.py the input image is getting undistorted.

<img src="https://user-images.githubusercontent.com/97686850/149366721-ad0d8a84-74f0-479b-89b1-9feadf9f3566.jpg" alt="Undistorted" width="200"/> <img src="https://user-images.githubusercontent.com/97686850/149368098-792a09dc-a845-45c5-b6ea-476f29f6f29e.jpg" alt="distorted Image" width="200"/> <img src="https://user-images.githubusercontent.com/97686850/149368104-8e7fec7d-e090-4f30-a57f-f23fda69b475.jpg" alt="Undistorted Image" width="200"/>


- After that the region of intested is being set. A lot of different lane detection projects use a trapezoid for the ROI, but this wasn't possible for this project since in turns the inner lane disappears and I need a the information that I get. ROI also helps with the computing power needed -> smaller images, faster computation 
<img src="https://user-images.githubusercontent.com/97686850/149367619-9e2eb325-7e0d-4078-a348-19fb4a7a3da3.jpg" alt="cropped image" width="300"/>

- The image process contains of canny edge detection and a threshold image. The combination of both is the combo_image and is used to warp the image. To visualize the lanes a hough transformation is used (right image)

<img src="https://user-images.githubusercontent.com/97686850/149367792-cda61e7b-4936-4127-b4db-3dbbff61aa8d.jpg" alt="canny image" width="200"/> <img src="https://user-images.githubusercontent.com/97686850/149367802-acd41c62-ab5b-4ef6-b19a-96919d7a5c5a.jpg" alt="theshold image" width="200"/> <img src="https://user-images.githubusercontent.com/97686850/149367814-31b56f55-e27b-45e8-bb73-7287b5a66472.jpg" alt="combo image" width="200"/> <img src="https://user-images.githubusercontent.com/97686850/149368778-b2768c91-5587-4a13-a646-9e840f66b7c7.jpg" alt="combo image" width="200"/>
- The warping of the image into a birdeye-view provids an optimal image perspective to extract the lane information especially in curved lanes.
 
<img src="https://user-images.githubusercontent.com/97686850/149368288-a6dd529f-3843-43e3-98d6-b4d264edb459.jpg" alt="birdeye image" width="300"/>

- To calculate the aimed trajectory the birdeye-image is being halfed. This halfed image is being scanned for the lanes. As a return a few middlepoints are generated and averaged. The trajectory is drawn into the birdeye-image from the middle of vehicle (bottom of the image) to the half of the image. As a x-value the averaged middlepoints is used. After that I rewarped the image to display the image in normal perspective as well!

<img src="https://user-images.githubusercontent.com/97686850/149368525-5bb016c5-b186-41cd-ac7d-1a9c2d07ffa3.jpg" alt="birdeye image with trajectory" width="300"/> <img src="https://user-images.githubusercontent.com/97686850/149368847-b1b54b88-1e55-47d1-82bd-4b0013009950.jpg" alt="image with trajectory" width="300"/>

- The detect_lanes_img function returnes the direction of the trajectory and the center of the car for a variance analysis.

- The last part is the implementation of a p-controller that is correcting the error between the trajectory and the middle of the car


**The workthrough of the obstacle detection is the following:**

- First you need a haar cascade for cars -> cars.xml
- After that take a reference image of an obstacle you want to detect
- Meassure the distance to the object and the width of the object and correct the variables KNOWN_DISTANCE and KNOWN_WIDTH
- Adjust the wanted distance before stopping
- After that drive onto the object and hope that all goes to play and nothing get's smashed :)
<img src="https://user-images.githubusercontent.com/97686850/149367499-2358dfd0-1710-4919-a26a-9a9ba0cfb66c.jpg" alt="Obstacle" width="300"/>  <img src="https://user-images.githubusercontent.com/97686850/149367440-03f757f5-0dde-49cd-9933-1abdf363bb12.jpg" alt="Obstacle" width="300"/>



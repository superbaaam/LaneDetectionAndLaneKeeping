import cv2
from easygopigo3 import EasyGoPiGo3
import random
# Colors
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX

# Inits
gpg = EasyGoPiGo3()
gpg.set_speed(80)
cap = cv2.VideoCapture(-1)

# Recorder
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640,480))


# car detector object
path = "/home/pi/gopi/code_v1/BachelorFinal/"
car_cascade = cv2.CascadeClassifier(f"{path}cars.xml")
print(car_cascade.empty())

# focal length finder function


def focal_length(measured_distance, real_width, width_in_rf_image):
    """
    This Function Calculate the Focal Length(distance between lens to CMOS sensor), it is simple constant we can find by using
    MEASURED_DISTACE, REAL_WIDTH(Actual width of object) and WIDTH_OF_OBJECT_IN_IMAGE
    :param1 Measure_Distance(int): It is distance measured from object to the Camera while Capturing Reference image

    :param2 Real_Width(int): It is Actual width of object, in real world (like My face width is = 14.3 centimeters)
    :param3 Width_In_Image(int): It is object width in the frame /image in our case in the reference image(found by Face detector)
    :retrun focal_length(Float):"""
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value


# distance estimation function
def distance_finder(focal_length, real_car_width, car_width_in_frame):
    """
    This Function simply Estimates the distance between object and camera using arguments(focal_length, Actual_object_width, Object_width_in_the_image)
    :param1 focal_length(float): return by the focal_length_Finder function

    :param2 Real_Width(int): It is Actual width of object, in real world (like My face width is = 5.7 Inches)
    :param3 object_Width_Frame(int): width of object in the image(frame in our case, using Video feed)
    :return Distance(float) : distance Estimated
    """
    distance = (real_car_width * focal_length) / car_width_in_frame
    return distance


# car detector function
def car_data(img):
    """
    This function Detect the car
    :param Takes image as argument.
    :returns car_width in the pixels
    """

    car_width = 0
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(
        gray_image, scaleFactor=1.22, minNeighbors=2, minSize=(150, 150))
    for (x, y, h, w) in cars:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
        car_width = w

    return car_width

# REFERENCES
# KNOWN_DISTANCE : distance from camera to object(face) measured
# KNOWN_WIDTH: width of car in the real world or Object Plane

# reading reference image from directory
#path_2 = "/home/pi/gopi/code_v1/Cam/"
#ref_image = cv2.imread(f"{path}reference.jpg")

# Modellauto Blues Brothers
# ref_image = cv2.imread(f"{path}reference_1.jpg")
# KNOWN_DISTANCE = 30   # centimeter
# KNOWN_WIDTH = 8  # centimeter


# Bild Käfer
ref_image = cv2.imread(f"{path}reference_2.jpg")
KNOWN_DISTANCE = 29   # centimeter
KNOWN_WIDTH = 6.5  # centimeter

# Bild Mustang
# ref_image = cv2.imread(f"{path}reference_3.jpg")
# KNOWN_DISTANCE = 29   # centimeter
# KNOWN_WIDTH = 7.5  # centimeter


ref_image_car_width = car_data(ref_image)
focal_length_found = focal_length(
    KNOWN_DISTANCE, KNOWN_WIDTH, ref_image_car_width)
# print(focal_length_found)
#cv2.imshow("ref_image", ref_image)


def main():
    letsgo = input("Bereit für die Erkennung? (Y/N) :   ")
    if letsgo == "Y" or letsgo == "y":
        gpg.forward()
        while True:
            _, frame = cap.read()
            rand = random.randrange(0, 101, 2)
            car_width_in_frame = car_data(frame)
            # print(car_width_in_frame)
            if car_width_in_frame == 0:
                Distance = 0
            elif car_width_in_frame != 0:
                Distance = distance_finder(
                    focal_length_found, KNOWN_WIDTH, car_width_in_frame)
                print("Distance :", Distance)
                # Drawing Text on the screen
                cv2.putText(
                    frame, f"Distance = {round(Distance,2)} CM", (50,
                                                                  50), fonts, 1, (WHITE), 2
                )
                cv2.imwrite(f"Screenshot{rand}.jpg", frame)
            print("Distance: ", Distance)
            cv2.imshow("frame", frame)

            # Abbruchbedingung!
            if Distance < 15 and Distance != 0:
                gpg.stop()

            if cv2.waitKey(1) == ord("q"):
                break
    else:
        print("Start over!")
    cap.release()
    # out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

#AUTHORS: Savannah Dare, Felix Quezada-York, Qi Cheng Feng, Helen Montero, Anna Keh 

#DATE: 12/25/2025
=======
#DATE: ssh rasp pi git rasp pi


#import libraries 
import time # so everything doesn't happen too fast
import board # so you can program the physical pins using names instead of numbers
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS # to program the accelerometer and gyroscope
from adafruit_lis3mdl import LIS3MDL # to program the magnetometer
from git import Repo # to interact with github
from picamera2 import Picamera2 # to program the camera
import os # so you can interact with the computer's operating system through code

#VARIABLES

THRESHOLD = 1.11154      #Any desired value from the accelerometer (that we manipulate), point is so that above a certain acceleration detected means the flatsat is actually being shaken

THRESHOLD = 1.11154      #Any desired value from the accelerometer

REPO_PATH = "/home/savannahdare/flatsat" #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "images"   #Your image folder path in your GitHub repo: ex. /Images, we don't do the stuff that comes before it just cause when we refer to it we'll merge it with the stuff that comes before it, and we don't include the slash because of the way that we merge them

#imu and camera initialization
i2c = board.I2C() # creates a communication channel so the rasp pi can talk to external sensors
accel_gyro = LSM6DS(i2c) # sets the accelerometer and gyroscope up as an object so you can refer to it in code easily, we're not using the gyroscope here the command that sets the accelerometer up as an object just happens to also set up the gyroscope as well
mag = LIS3MDL(i2c) # sets the magnetometer up as an object so you can refer to it in code easily, we're not actually using the magnetometer in the flatsat we just have it here so we can copy and paste later for cubesat
picam2 = Picamera2() # sets the camera up as an object so you can refer to it in code easily


def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try: # the try and except stuff; try attempts at certain code, if it fails except will print a more clean error message
        repo = Repo(REPO_PATH) # stores the local repository as an object in the code so it can be manipulated more easily
        origin = repo.remote('origin') # stores the corresponding remote repository as an object for same reason
        print('added remote')
        origin.pull() # pull in changes from github in case someone pushed an edit there
        print('pulled changes')
        repo.git.add(os.path.join(REPO_PATH, FOLDER_PATH)) # add the updates of image folder to be tracked by git
        repo.index.commit('New Photo') # commit, each commit is named 'New Photo'
        print('made the commit')
        origin.push() # push changes to github
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')


def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S") # obtains the time in a certain format
    return os.path.join(REPO_PATH, FOLDER_PATH, f"{name}{t}.jpg") # creates a path in the repository, takes repo path, then images folder path, and then the path in that folder to the specific image

def take_photo():
    """
    Takes a photo when acceleration magnitude exceeds THRESHOLD.
    Correct implementation for Raspberry Pi Camera Module 3.
    """

    # ---- Camera setup (ONCE) ----
    capture_config = picam2.create_still_configuration() # creates a camera setup optimized for taking a photo, pre-set resolution pixel format etc
    picam2.configure(capture_config) # loads the camera settings you defined in previous setting to load them into the camera system
    picam2.start() # cam is now ready to take a pic
    time.sleep(2)  # Allow camera to warm up

    while True:

        accelx, accely, accelz = accel_gyro.acceleration # makes 3 variables for acceleration in each axis loaded from the accelerometer
        mag_accel = (accelx**2 + accely**2 + accelz**2) ** 0.5 # math that determines the ultimate acceleration
        dynamic_accel = abs(9.81-mag_accel) # calculates acceleration deviating from gravitational acceleration

        accelx, accely, accelz = accel_gyro.acceleration
        mag_accel = (accelx**2 + accely**2 + accelz**2) ** 0.5
        dynamic_accel = abs(9.81-mag_accel)


        if dynamic_accel > THRESHOLD:
            time.sleep(0.5)  # debounce delay
            name = "SavannahD" # stores name which is used for generating name of image
            image_name = img_gen(name) # actually creates the file path for the image
            picam2.capture_file(image_name) # captures an image storing it in that file path made in the last line
            git_push() # push all changes to github
            time.sleep(2)  # prevent rapid re-triggering
        time.sleep(0.1) #pause



def main(): # main function, function that runs everything that needs to be run in the right order
    take_photo() # runs take_photo function 



if __name__ == '__main__': # runs the main function within the condition that the program was run directly
    main()

if __name__ == '__main__':
    main()


from PathMoverUtils import run_path_follower
import ServoUtil
from detect_object import detect_color_shape
from time import sleep
import ImageUtils
import UltrasonicUtils
import MotorUtils


#TODO define
DISTANCE_THRESHOLD = 20


def pickObject():
    MotorUtils.set_all_servos(137, 180)
    sleep(0.5)
    MotorUtils.set_all_servos(137, 180, 55)
    sleep(2)
    MotorUtils.set_all_servos(120, 180)


def rotateInDirection(dir, isSmall):
    timeToMove = 0.1
    if isSmall:
        timeToMove = 0.05
    if dir == "left":
        MotorUtils.rotate_left(timeToMove)

    elif dir == "right":
        MotorUtils.rotate_right(timeToMove)


def moveForward():
    MotorUtils.front(0.1)



def isDistanceReached():
    return UltrasonicUtils.getNormalizedDistance() <= DISTANCE_THRESHOLD

class Bot:
    def __init__(self):
        pass

    def look_at_line(self):
        ServoUtil.make_camera_look_at_floor()

    def follow_line(self):
    
        self.look_at_line()
        sleep(0.5)
        aruco = run_path_follower()
        return aruco
    

    def seek_object(self, rotate_direction):
        ServoUtil.make_camera_look_at_object()
        while True:
            sleep(0.5)
            color = 'red'
            image = ImageUtils.get_frame()
            present, dir = detect_color_shape(image, color, "cube")

            if not present or (present and dir != "center"):
                if not present:
                    rotateInDirection(rotate_direction, False)
                else:
                    rotateInDirection(dir, True)
                continue
            else:
                if not isDistanceReached() :
                    moveForward()
                else:
                    pickObject()
                    break



    




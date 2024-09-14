
from UltrasonicUtils import getNormalizedDistance
from MotorUtils import front, rotate_left, rotate_right, set_all_servos
from time import sleep
from ImageUtils import get_frame
from detect_object import detect_color_shape
from TaskRunner import pickObject

#TODO define
DISTANCE_THRESHOLD = 20

def setArmPostions():
    set_all_servos(30, 180, 90)
    sleep(1)
    set_all_servos(75, 180)
    sleep(1)
    set_all_servos(125, 180)
    sleep(0.5)

def isObjectPresent(color):
    ip = input("give image detection input")
    ip = ip.split(',')
    if len(ip) != 2:
        print("invalid")
        return 
    present = False
    if ip[0] == 't':
        present = True
    else:
        present = False
    dir = None
    if  ip[1] == 'c':    
        dir = "center"
    elif ip[1] == 'r':
        dir = "right"
    elif ip[1] == "l":
        dir = "left"

    return present, dir


def isDistanceReached():
    return getNormalizedDistance() <= DISTANCE_THRESHOLD


def rotateInDirection(dir, isSmall):
    timeToMove = 0.1
    if isSmall:
        timeToMove = 0.05
    if dir == "left":
        rotate_left(timeToMove)

    elif dir == "right":
        rotate_right(timeToMove)
    

def moveForward():
    front(0.1)

# Assuming init done
# expectation is that, the bot is coming and stopping close the the box.
def moveTillObject(rotateDirection):

    while True:
        sleep(0.5)
        color = 'red'
        image = get_frame()
        present, dir = detect_color_shape(image, color, "cube")

        if not present or (present and dir != "center"):
            if not present:
                rotateInDirection(rotateDirection, False)
            else:
                rotateInDirection(dir, True)
            continue
        else:
            if not isDistanceReached() :
                moveForward()
            else:
                pickObject()
                break


def init():
    setArmPostions()

if __name__ == '__main__':
    init()
    moveTillObject("left")
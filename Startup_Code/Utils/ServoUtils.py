from Utils.MotorUtils import set_all_servos
from time import sleep

RESET_MAIN_ARM = 30
RESET_CAMERA_ARM = 60
RESET_GRIPPER_ARM = 100

OBJECT_FOLLOW_MAIN_ARM = 50 # was 95
OBJECT_FOLLOW_CAMERA_ARM = 65 # was 135

OBJECT_PICKUP_MAIN_ARM = 137
OBJECT_PICKUP_CAMERA_ARM = 180
OBJECT_PICKUP_GRIPPER_ARM = 55

OBJECT_DROP_MAIN_ARM = 137
OBJECT_DROP_CAMERA_ARM = 180 # was 150
OBJECT_DROP_GRIPPER_ARM = 80

MARKER_RETURN_MAIN_ARM = 50
MARKER_RETURN_CAMERA_ARM = 67

READ_BILLBOARD_MAIN_ARM = 85
READ_BILLBOARD_CAMERA_ARM = 160 # try 175 to work for all distances

PEN_UP_MAIN_ARM = 90
PEN_DOWN_MAIN_ARM = 150

LINE_FOLLOW_MAIN_ARM = 50
LINE_FOLLOW_CAMERA_ARM = 0


def reset_arms(set_gripper=False):
    print("reset called")
    sleep(0.5)
    if set_gripper is True:
        set_all_servos(RESET_MAIN_ARM, RESET_CAMERA_ARM, RESET_GRIPPER_ARM)
    else:
        set_all_servos(RESET_MAIN_ARM, RESET_CAMERA_ARM)
    sleep(0.5)
    return


def make_camera_look_at_floor():
    set_all_servos(LINE_FOLLOW_MAIN_ARM, LINE_FOLLOW_CAMERA_ARM)
    sleep(1)
    return


def make_camera_look_at_object():
    set_all_servos(60, 90)
    sleep(1)
    set_all_servos(OBJECT_FOLLOW_MAIN_ARM, OBJECT_FOLLOW_CAMERA_ARM)
    sleep(0.5)

def make_camera_look_at_billboard():
    set_all_servos(60, 90)
    sleep(1)
    set_all_servos(READ_BILLBOARD_MAIN_ARM, READ_BILLBOARD_CAMERA_ARM)
    sleep(0.5)


def make_camera_look_at_marker():
    set_all_servos(60, 90)
    sleep(1)
    set_all_servos(MARKER_RETURN_MAIN_ARM, MARKER_RETURN_CAMERA_ARM)
    sleep(0.5)

def pick_object():
    set_all_servos(OBJECT_PICKUP_MAIN_ARM, OBJECT_PICKUP_CAMERA_ARM)
    sleep(0.5)
    set_all_servos(OBJECT_PICKUP_MAIN_ARM, OBJECT_PICKUP_CAMERA_ARM, OBJECT_PICKUP_GRIPPER_ARM)
    sleep(2)
    #earlier it was 120
    set_all_servos(90, 180)

def drop_object():
    set_all_servos(OBJECT_DROP_MAIN_ARM, OBJECT_DROP_CAMERA_ARM)
    sleep(0.5)
    set_all_servos(OBJECT_DROP_MAIN_ARM, OBJECT_DROP_CAMERA_ARM, OBJECT_DROP_GRIPPER_ARM)
    sleep(2)
    #earlier it was 120
    set_all_servos(90, 180)

def pen_up():
    set_all_servos(PEN_UP_MAIN_ARM, 180)
    sleep(0.5)

def pen_down():
    set_all_servos(PEN_DOWN_MAIN_ARM, 180)
    sleep(0.5)

if __name__ == "__main__" :
    make_camera_look_at_floor()

from Utils.MotorUtils import set_all_servos
from time import sleep

RESET_MAIN_ARM = 30
RESET_CAMERA_ARM = 60
RESET_GRIPPER_ARM = 100

OBJECT_FOLLOW_MAIN_ARM = 95
OBJECT_FOLLOW_CAMERA_ARM = 135

MARKER_RETURN_MAIN_ARM = 95
MARKER_RETURN_CAMERA_ARM =135
LINE_FOLLOW_MAIN_ARM = 90
LINE_FOLLOW_CAMERA_ARM = 30

def reset_arms(set_gripper=False):
    if set_gripper is True:
        set_all_servos(RESET_MAIN_ARM, RESET_CAMERA_ARM, RESET_GRIPPER_ARM)
    else:
        set_all_servos(RESET_MAIN_ARM, RESET_CAMERA_ARM)
    return


def make_camera_look_at_floor():
    reset_arms()
    sleep(2)
    set_all_servos(LINE_FOLLOW_MAIN_ARM, LINE_FOLLOW_CAMERA_ARM)
    return


def make_camera_look_at_object():
    set_all_servos(RESET_MAIN_ARM, RESET_CAMERA_ARM, RESET_GRIPPER_ARM)
    sleep(1)
    set_all_servos(60, 90)
    sleep(1)
    set_all_servos(OBJECT_FOLLOW_MAIN_ARM, OBJECT_FOLLOW_CAMERA_ARM)
    sleep(0.5)

def make_camera_look_at_marker():
    set_all_servos(RESET_MAIN_ARM, RESET_CAMERA_ARM)
    sleep(1)
    set_all_servos(60, 90)
    sleep(1)
    set_all_servos(MARKER_RETURN_MAIN_ARM, MARKER_RETURN_CAMERA_ARM)
    sleep(0.5)


if __name__ == "__main__" :
    make_camera_look_at_floor()

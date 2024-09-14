import cv2
import numpy as np
from time import sleep
from ARTagUtils import detect_aruco_markers, MarkerAction
from ImageUtils import get_frame, IMG_WIDTH, IMG_HEIGHT, FRAME_MODE
from BoxPositionsTester import NUM_BOXES, load_positions_from_file, generate_segments, display_image_with_segments
if (FRAME_MODE == 1):  # Camera mode, running on Pi
    from MotorUtils import front, rotate_right, rotate_left, back, strafe_left, strafe_right, stop
from MotorUtils import *
from PathMoverUtils import run_path_follower

# Distance between AR to bill board -> 30 - 40 cm
# Height of box from which you have to pick object -> 10cm
# Height of indicator to come back to path -> 5cm
# Size of box in which you have to drop object - 8cm by 8cm
# Height of the indicator to drop the object -> 5cm
# Height of billboard (topmost point and lowest point) -> 25 and 7cm respectively
# Object to Pick -> cube of side 2.8cm (same for marker)

def reset_arms(set_gripper=False):
    if set_gripper is True:
        set_all_servos(30,60,90)
    else:
        set_all_servos(30,60)
    return

def make_camera_look_at_floor():
    reset_arms()
    set_all_servos(120,15)
    return

def read_billboard_1():
    # as soon as bot finds marker it stops there and calls this function
    # so we have to go to billboard (common function), read it
    front()
    return

def pick_object_left():
    return

def pick_object_right():
    return

def return_to_path():
    return

def drop_object_left():
    return

def drop_object_right():
    return

def read_billboard_2():
    return

def read_billboard_3():
    return

def execute_lane():
    return

def write_letter():
    return

def execute_marker_action(action):
    if action == MarkerAction.NONE:
        return None
    elif action == MarkerAction.READ_BILLBOARD_1:
        read_billboard_1()
        print("Read billboard 1")
    elif action == MarkerAction.PICK_OBJECT_LEFT:
        pick_object_left()
        print("Pick object - Left")
    elif action == MarkerAction.PICK_OBJECT_RIGHT:
        pick_object_right()
        print("Pick object - Right")
    elif action == MarkerAction.DROP_OBJECT_LEFT:
        drop_object_left()
        print("Drop object - Left")
    elif action == MarkerAction.DROP_OBJECT_RIGHT:
        drop_object_right()
        print("Drop object - Right")
    elif action == MarkerAction.READ_BILLBOARD_2:
        read_billboard_2()
        print("Read billboard 2")
    elif action == MarkerAction.EXECUTE_LANE:  
        execute_lane() 
        print("Execute lane")
    elif action == MarkerAction.READ_BILLBOARD_3:
        read_billboard_3()
        print("Read billboard 3")
    elif action == MarkerAction.WRITE_LETTER:
        write_letter()
        print("Write letter")
    else:
        print("No action")

marker_actions = [MarkerAction.NONE, MarkerAction.READ_BILLBOARD_1, MarkerAction.PICK_OBJECT_LEFT, MarkerAction.PICK_OBJECT_RIGHT,
                  MarkerAction.DROP_OBJECT_LEFT, MarkerAction.DROP_OBJECT_RIGHT, MarkerAction.READ_BILLBOARD_2, 
                  MarkerAction.EXECUTE_LANE,MarkerAction.READ_BILLBOARD_3, MarkerAction.WRITE_LETTER]

if __name__ == '__main__':
    start = False
    
    try:
        while True:
            if start is False:
                reset_arms(True)
                make_camera_look_at_floor() 
                start = True
            # Returns when a marker is detected, if image is None, or if any key is pressed
            runner = run_path_follower()
            if runner in marker_actions:
                execute_marker_action(runner)
                # Run action on detecting the marker
                break
            elif runner is None:
                print("Did not get the frame or Exit on any key press")
                break

    except KeyboardInterrupt:
        stop()
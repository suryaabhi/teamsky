from detect_object import detect_color_shape
from time import sleep

from Utils.PathMoverUtils import run_path_follower

import Utils.ServoUtils as ServoUtils
import Utils.ImageUtils as ImageUtils
import Utils.UltrasonicUtils as UltrasonicUtils
import Utils.MotorUtils as MotorUtils

#TODO define
DISTANCE_THRESHOLD = 20
PATH_FINDER_OBJECT_COLOR = "orange"
PATH_FINDER_OBJECT_SHAPE = "circle"

class Bot:
    def __init__(self):
        self.pick_color = None
        self.pick_shape = None
        self.drop_color = None
        self.drop_shape = None

        self.intersection_answer = None

        self.draw_answer = None
        pass

    def __rotateInDirection(self, dir, isSmall):
        timeToMove = 0.1
        if isSmall:
            timeToMove = 0.05
        if dir == "left":
            MotorUtils.rotate_left(timeToMove)

        elif dir == "right":
            MotorUtils.rotate_right(timeToMove)
    

    def __pickObject(self):
        MotorUtils.set_all_servos(137, 180)
        sleep(0.5)
        MotorUtils.set_all_servos(137, 180, 55)
        sleep(2)
        MotorUtils.set_all_servos(120, 180)

    def __moveForward(self):
        MotorUtils.front(0.1)

    def __isDistanceReached(self):
        return UltrasonicUtils.getNormalizedDistance() <= DISTANCE_THRESHOLD

    def read_billboard_1(self):
        self.pick_color = "red"
        self.pick_shape = "circle"
        self.drop_color = "blue"
        self.drop_shape = "square"
        pass
    
    def read_billboard_2(self):
        self.intersection_answer = "left"
        pass
    
    def read_billboard_3(self):
        self.draw_answer = "3C"
        pass

    def __look_at_line(self):
        ServoUtils.make_camera_look_at_floor()

    def follow_line(self):
        self.__look_at_line()
        sleep(0.5)
        aruco = run_path_follower()
        return aruco

    def find_way_back_to_path(self):
        self.__seek_pathfinder_object()
        self.__find_line()
        self.follow_line()
        pass

    def move_to_answer_path(self):
        pass

    def draw_object(self):
        pass

    def seek_and_pick_object(self, rotate_direction):
        object_color = self.pick_color
        object_shape = self.pick_shape
        ServoUtils.make_camera_look_at_object()
        while True:
            sleep(0.2)
            image = ImageUtils.get_frame()
            present, dir = detect_color_shape(image, object_color, object_shape)

            if not present or (present and dir != "center"):
                if not present:
                    self.__rotateInDirection(rotate_direction, False)
                else:
                    self.__rotateInDirection(dir, True)
                continue
            else:
                if not self.__isDistanceReached() :
                    self.__moveForward()
                else:
                    self.__pickObject()
                    break

    def seek_and_drop_object(self, rotate_direction):
        '''
        UNTESTED CODE WRITTEN BY COPILOT
        DO NOT RUN WITHOUT VERIFICATION
        '''
        object_color = self.drop_color
        object_shape = self.drop_shape
        ServoUtils.make_camera_look_at_object()
        while True:
            sleep(0.2)
            image = ImageUtils.get_frame()
            present, dir = detect_color_shape(image, object_color, object_shape)

            if not present or (present and dir != "center"):
                if not present:
                    self.__rotateInDirection(rotate_direction, False)
                else:
                    self.__rotateInDirection(dir, True)
                continue
            else:
                if not self.__isDistanceReached():
                    self.__moveForward()
                else:
                    MotorUtils.set_all_servos(137, 180, 55)
                    sleep(2)
                    MotorUtils.set_all_servos(120, 180)
                    break

    

from detect_object import detect_color_shape
from time import sleep
import cv2
from Utils.PathMoverUtils import run_path_follower, is_path_found
from llm import send_to_llm_bb1
import Utils.ServoUtils as ServoUtils
import Utils.ImageUtils as ImageUtils
import Utils.UltrasonicUtils as UltrasonicUtils
import Utils.MotorUtils as MotorUtils

# driver to test code 
def detect_return_marker():
    pass


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
        #earlier it was 120
        MotorUtils.set_all_servos(90, 180)
     

            
    def pickpen(self):
        MotorUtils.set_all_servos(137, 180)
        sleep(0.5)
        MotorUtils.set_all_servos(137, 180, 55)
        sleep(2)
        MotorUtils.set_all_servos(120, 180)
        sleep(2)
        MotorUtils.set_all_servos(120,180,40)
        sleep(1)
        MotorUtils.set_all_servos(155,180)

    def __oppositeDir(self, dir):
        if dir == "right":
            return "left"
        return "right"
    
    def searchPath(self):
        self.__look_at_line()
        return is_path_found()


    def __moveForward(self, speed=0.1):
        MotorUtils.front(speed)

    def __moveBackward(self):
        MotorUtils.back(0.3)

    def __isDistanceReached(self):
        return UltrasonicUtils.getNormalizedDistance() <= DISTANCE_THRESHOLD

    def read_billboard_1(self):
        image = ImageUtils.get_frame()
        llm_resp = send_to_llm_bb1(image)
        print(llm_resp)
        if not llm_resp["found"]:
            return
        self.pick_color = llm_resp["pick"]["color"]
        self.pick_shape = llm_resp["pick"]["shape"]
        self.drop_color = llm_resp["drop"]["color"]
        self.drop_shape = llm_resp["drop"]["shape"]
    
    def read_billboard_2(self):
        self.intersection_answer = "left"
        pass
    
    def read_billboard_3(self):
        self.draw_answer = "3C"
        pass

    def __look_at_line(self):
        ServoUtils.make_camera_look_at_floor()

    def __look_at_return_marker(self):
        ServoUtils.make_camera_look_at_object()

    
    def follow_line(self):
        ServoUtils.reset_arms()
        self.__look_at_line()
        sleep(0.5)
        aruco = run_path_follower()
        return aruco

    def find_way_back_to_path(self, rotate_direction):

        self.__look_at_return_marker()
        while True:
            image = ImageUtils.get_frame()
            present, dir = detect_color_shape(image, "red", "square")

            if not present or (present and dir != "center"):
                if not present:
                    self.__rotateInDirection(rotate_direction, False)
                    sleep(0.2)
                else:
                    self.__rotateInDirection(dir, True)
                    sleep(0.2)
                continue
            else:
                self.__moveForward(0.3)
                if self.searchPath():
                    return
                self.__look_at_return_marker()

        

    def move_to_answer_path(self):
        pass

    def draw_object(self):
        pass

    def seek_and_pick_object(self, rotate_direction):
        object_color = self.pick_color
        object_shape = self.pick_shape
        ServoUtils.reset_arms(True)
        sleep(2)
        ServoUtils.make_camera_look_at_object()
        while True:
            sleep(0.2)
            image = ImageUtils.get_frame()
            present, dir = detect_color_shape(image, "blue", "square")

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
                    sleep(1)
                    self.__moveBackward()
                    sleep(1)
                    self.__rotateInDirection( self.__oppositeDir(rotate_direction) , False )
                    break

    def seek_and_drop_object(self, rotate_direction):
        '''
        UNTESTED CODE WRITTEN BY COPILOT
        DO NOT RUN WITHOUT VERIFICATION
        '''
        object_color = self.drop_color
        object_shape = self.drop_shape
        ServoUtils.reset_arms()
        sleep(2)
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

    

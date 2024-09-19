from detect_object import detect_color_shape
from time import sleep
import cv2
from Utils.PathMoverUtils import run_path_follower, is_path_found, rotate_right_until_road_found, rotate_left_until_road_found
import llm
import Utils.ServoUtils as ServoUtils
import Utils.ImageUtils as ImageUtils
import Utils.UltrasonicUtils as UltrasonicUtils
import Utils.MotorUtils as MotorUtils
from write_letter import write_letter

# driver to test code 
def detect_return_marker():
    pass


#TODO define
PATH_FINDER_OBJECT_COLOR = "red"
PATH_FINDER_OBJECT_SHAPE = "circle"

MARKER_OBJECT_COLOR = "red"
MARKER_OBJECT_SHAPE = "square"

#KRITIKA/VINIT
PICK_OBJECT_FALLBACK_COLOR = "blue"
PICK_OBJECT_FALLBACK_SHAPE = "square"
DROP_OBJECT_FALLBACK_COLOR = "green"
DROP_OBJECT_FALLBACK_SHAPE = "circle"

class Bot:
    def __init__(self):
        self.pick_color= PICK_OBJECT_FALLBACK_COLOR
        self.pick_shape = PICK_OBJECT_FALLBACK_SHAPE
        self.drop_color = DROP_OBJECT_FALLBACK_COLOR
        self.drop_shape= DROP_OBJECT_FALLBACK_SHAPE
        self.intersection_answer = "right"
        self.intersection_visited = 0
        self.draw_answer = ["3", "C"]


    def __rotateInDirection(self, dir, isSmall):
        timeToMove = 0.1
        if isSmall:
            timeToMove = 0.05
        if dir == "left":
            MotorUtils.rotate_left(timeToMove)

        elif dir == "right":
            MotorUtils.rotate_right(timeToMove)

    def __pickObject(self):
        ServoUtils.pick_object()
     
    def __dropObject(self):
        ServoUtils.drop_object()

    def isValidShape(self, shape):
        return shape in ["square", "circle"]
    
    def isValidColor(self, color):
        return color  in ["red", "blue", "green" s]

            
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

    def oppositeDir(self, dir):
        if dir == "right":
            return "left"
        return "right"
    
    def searchPath(self):
        self.__look_at_line()
        return is_path_found()


    def moveForward(self, speed=0.1):
        MotorUtils.front(speed)

    def moveBackward(self):
        MotorUtils.back(0.3)

    def __isDistanceReached(self, distance_threshold = 20):
        return UltrasonicUtils.getNormalizedDistance() <= distance_threshold
        # return distanceSensor.getDistance() <= distance_threshold

    def __isBeyondDistance(self, max_distance = 17):
        return UltrasonicUtils.getNormalizedDistance() <= max_distance

    def read_billboard_1(self):
        ServoUtils.make_camera_look_at_billboard()
        image = ImageUtils.get_frame()
        llm_resp = llm.send_to_llm_bb1(image)
        print(llm_resp)
        if not llm_resp["found"]:
            #TODO retry
            self.moveForward(0.3)
            return False
        
        self.pick_color = llm_resp["pick"]["color"] if self.isValidColor(llm_resp["pick"]["color"]) else PICK_OBJECT_FALLBACK_COLOR
        self.pick_shape = llm_resp["pick"]["shape"] if self.isValidShape(llm_resp["pick"]["shape"]) else PICK_OBJECT_FALLBACK_SHAPE
        self.drop_color = llm_resp["drop"]["color"] if self.isValidColor(llm_resp["drop"]["color"]) else DROP_OBJECT_FALLBACK_COLOR
        self.drop_shape = llm_resp["drop"]["shape"] if self.isValidShape(llm_resp["drop"]["shape"]) else DROP_OBJECT_FALLBACK_SHAPE
        sleep(0.5)
        self.moveForward(0.3)
        sleep(0.5)
        return True
    
    def read_billboard_2(self):
        ServoUtils.make_camera_look_at_billboard()
        image = ImageUtils.get_frame()
        llm_resp = llm.send_to_llm_bb2(image)
        print(llm_resp)
        if not llm_resp["found"]:
            return
        self.intersection_answer = llm_resp["path"]
        sleep(0.5)
        self.moveForward(0.3)
        sleep(0.5)
        pass
    
    def read_billboard_3(self):
        image = ImageUtils.get_frame()
        llm_resp = llm.send_to_llm_bb3(image)
        print(llm_resp)
        self.draw_answer = llm_resp["characters"]
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
            present, dir = detect_color_shape(image, PATH_FINDER_OBJECT_COLOR, PATH_FINDER_OBJECT_SHAPE, 40)

            if not present or (present and dir != "center"):
                if not present:
                    self.__rotateInDirection(rotate_direction, False)
                    sleep(0.2)
                else:
                    self.__rotateInDirection(dir, True)
                    sleep(0.2)
                continue
            else:
                self.moveForward(0.3)
                if self.searchPath():
                    if rotate_direction == "left":
                        self.moveForward(0.35)
                        rotate_right_until_road_found()
                        sleep(1)
                    else:
                        self.moveForward(0.35)
                        rotate_left_until_road_found()
                        sleep(1)
                    return
                self.__look_at_return_marker()


    def find_way_back_to_path_ultrasonic(self, rotate_direction):

        self.__look_at_return_marker()
        while True:
            image = ImageUtils.get_frame()
            present, dir = detect_color_shape(image, PATH_FINDER_OBJECT_COLOR, PATH_FINDER_OBJECT_SHAPE, 40)

            if not present or (present and dir != "center"):
                if not present:
                    self.__rotateInDirection(rotate_direction, False)
                    sleep(0.2)
                else:
                    self.__rotateInDirection(dir, True)
                    sleep(0.2)
                continue
            else:
                if not self.__isDistanceReached(30) :
                    self.moveForward(0.3)
                else:
                    if self.searchPath():
                        if rotate_direction == "left":
                            self.moveForward(0.35)
                            rotate_right_until_road_found()
                            sleep(1)
                        else:
                            self.moveForward(0.35)
                            rotate_left_until_road_found()
                            sleep(1)
                        return
                

    def execute_lane(self):
        if self.intersection_visited == 0:
            self.intersection_visited = 1
            if self.intersection_answer == "left":
                MotorUtils.rotate_left(0.3)
                sleep(0.5)
                self.moveForward(1.8)
                sleep(0.5)
                rotate_left_until_road_found()
                sleep(0.5)
            elif self.intersection_answer == "right":
                MotorUtils.rotate_right(0.3)
                sleep(0.5)
                self.moveForward(1.8)
                sleep(0.5)
                rotate_right_until_road_found()
                sleep(0.5)
            else:
                self.moveForward(1.8)
        elif self.intersection_visited == 1:
            self.intersection_visited = 2
            if self.intersection_answer == "left":
                MotorUtils.rotate_left(0.4)
                sleep(0.5)
                self.moveForward(1)
                sleep(0.5)
                rotate_left_until_road_found()
                sleep(0.5)
            elif self.intersection_answer == "right":
                MotorUtils.rotate_right(0.4)
                sleep(0.5)
                self.moveForward(1)
                sleep(0.5)
                rotate_right_until_road_found()
                sleep(0.5)
            else:
                self.moveForward(1.8)
        

    def move_to_answer_path(self):
        pass

    def draw_object(self):
        pass

    def seek_and_pick_object(self, rotate_direction, pick_marker = False):
        if not pick_marker:
            object_color = self.pick_color
            object_shape = self.pick_shape
        else:
            object_color = MARKER_OBJECT_COLOR
            object_shape = MARKER_OBJECT_SHAPE
        ServoUtils.reset_arms(True)
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
                if not self.__isDistanceReached() :
                    self.moveForward()
                elif self.__isBeyondDistance():
                    self.moveBackward()
                else:
                    self.__pickObject()
                    sleep(1)
                    self.moveBackward()
                    sleep(1)
                    self.__rotateInDirection( self.oppositeDir(rotate_direction) , False )
                    break

    def seek_and_drop_object(self, rotate_direction):
        object_color = self.drop_color
        object_shape = self.drop_shape
   
        ServoUtils.reset_arms()
        sleep(2)
        ServoUtils.make_camera_look_at_marker()
        while True:
            sleep(0.2)
            image = ImageUtils.get_frame()
            present, dir = detect_color_shape(image, object_color, object_shape, 30)

            if not present or (present and dir != "center"):
                if not present:
                    self.__rotateInDirection(rotate_direction, False)
                else:
                    self.__rotateInDirection(dir, True)
                continue
            else:
                if not self.__isDistanceReached(21):
                    self.moveForward()
                elif self.__isBeyondDistance():
                    self.moveBackward()
                else:
                    self.__dropObject()
                    self.moveBackward()
                    sleep(1)
                    self.__rotateInDirection( self.oppositeDir(rotate_direction) , False )
                    break

    def write(self):
        MotorUtils.rotate_right(0.5)
        sleep(1)
        self.moveForward(0.2)
        sleep(1)
        
        for letter in self.draw_answer:
            write_letter(letter)
            sleep(2)

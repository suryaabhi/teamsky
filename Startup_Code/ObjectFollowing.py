
from UltrasonicUtils import getNormalizedDistance
from MotorUtils import front, rotate_left, rotate_right, set_all_servos
from time import sleep
from ImageUtils import get_frame
from detect_object import detect_color_shape
from TaskRunner import pickObject




# def isObjectPresent(color):
#     ip = input("give image detection input")
#     ip = ip.split(',')
#     if len(ip) != 2:
#         print("invalid")
#         return 
#     present = False
#     if ip[0] == 't':
#         present = True
#     else:
#         present = False
#     dir = None
#     if  ip[1] == 'c':    
#         dir = "center"
#     elif ip[1] == 'r':
#         dir = "right"
#     elif ip[1] == "l":
#         dir = "left"

#     return present, dir

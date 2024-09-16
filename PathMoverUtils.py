import cv2
import numpy as np
from time import sleep
from ARTagUtils import detect_aruco_markers, MarkerAction
from ImageUtils import get_frame, IMG_WIDTH, IMG_HEIGHT, FRAME_MODE
from BoxPositionsTester import NUM_BOXES, load_positions_from_file, generate_segments, display_image_with_segments
if (FRAME_MODE == 1):  # Camera mode, running on Pi
    from Utils.MotorUtils import front, rotate_right, rotate_left, back, strafe_left, strafe_right, stop
box_positions = None
# Image Processing Constants
GAUSSIAN_BLUR_PIXEL_SIZE = 5
MORPH_RECTANGLE_PIXEL_SIZE = 10
VERY_DARK_GRAY_THRESHOLD = 70
# Bot Movement Constants
SMALL_TURN = 25  # Degrees to turn
SMALL_STEP = 0.1  # Time in seconds for small front movement
ADJUST_THRESHOLD = 10  # Value in degrees above which we adjust
# Area threshold for detecting - adj left/ adj right / straight
ADJ_AREA_THRESHOLD = 0.1
# Area threshold for detecting left / right / straight options exist
PATH_EXISTS_AREA_THRESHOLD = 0.5
BOT_OFFSET = 250  # Offset from the bottom of the frame to the bot center
bot_center = np.array([int(IMG_WIDTH/2), int(IMG_HEIGHT + BOT_OFFSET)])
ROTATION_IN_1_SEC = 180  # In degrees
 
 
def thresholding(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(
        gray, (GAUSSIAN_BLUR_PIXEL_SIZE, GAUSSIAN_BLUR_PIXEL_SIZE), 0)
 
    # Apply a global threshold to detect very dark gray and black regions
    _, thresholded = cv2.threshold(
        blurred, VERY_DARK_GRAY_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
 
    # Apply morphological operations
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (MORPH_RECTANGLE_PIXEL_SIZE, MORPH_RECTANGLE_PIXEL_SIZE))
    morph = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)
    return morph
 
 
def get_contour_info(segment):
    # Find all contours in the frame
    contours, _ = cv2.findContours(
        segment.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
 
    total_area = 0
    total_cx = 0
    total_cy = 0
 
    # Iterate through all contours
    for contour in contours:
        area = cv2.contourArea(contour)
        total_area += area
 
        # Calculate moments for each contour
        M = cv2.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
 
            # Weight the centroid by the area of the contour
            total_cx += cx * area
            total_cy += cy * area
 
    # Calculate the combined centroid by dividing the weighted sum by the total area
    if total_area != 0:
        combined_cx = int(total_cx / total_area)
        combined_cy = int(total_cy / total_area)
    else:
        combined_cx, combined_cy = 0, 0
 
    return total_area, (combined_cx, combined_cy)
 
 
def process_segments(segments, frame):
    contour_dict = {f'box{i}': (0, (0, 0))
                    for i in range(1, NUM_BOXES + 1)}
 
    for box_name, segment in segments.items():
        contour_dict[box_name] = get_contour_info(segment)
        if box_name in ['bottom']:
            cv2.circle(
                segments[box_name], contour_dict[box_name][1], 3, (128, 255, 0), thickness=-1)
 
    cv2.circle(
        frame, bot_center, 3, (128, 255, 0), thickness=-1)
    display_image_with_segments(frame, segments)
    return contour_dict
 
 
def get_current_road_node(contour_dict):
    result = ''
    # Bottom box is larger so area threshold is lower
    canContinueStraight = False
    if contour_dict['bottom'][0] >= ADJ_AREA_THRESHOLD * box_positions['bottom']['width'] * box_positions['bottom']['height']:
        # There is path ahead
        top_box_center = np.add(
            (box_positions['bottom']['x'], box_positions['bottom']['y']),
            contour_dict['bottom'][1])
        delta = abs(IMG_WIDTH/2 - top_box_center[0])
 
        # Prioritize adjusting over turning
        if delta > 25 and top_box_center[0] < IMG_WIDTH/2:
            return 'adj_left', delta
        elif delta > 25:
            return 'adj_right', delta
        canContinueStraight = True
 
    if contour_dict['left'][0] >= 0.5 * box_positions['left']['width'] * box_positions['left']['height']:
        # There is a path to the left
        result += 'left'
    if contour_dict['right'][0] >= 0.5 * box_positions['right']['width'] * box_positions['right']['height']:
        # There is a path to the right
        result += 'right'
 
    if result == '':
        if canContinueStraight:
            return 'continue', None
        else:
            return 'deadend', None
    else:
        if contour_dict['center'][0] > PATH_EXISTS_AREA_THRESHOLD * box_positions['center']['width'] * box_positions['center']['height']:
            result += 'straight'
    return result, None
 
 
def turn_left():
    move_front_until_clear(True)
    sleep(0.5)
    front(0.3)
    while True:
        contour_dict = get_contours_from_frame(get_frame())
        if contour_dict['left'][0] >= 0.1 * box_positions['left']['width'] * box_positions['left']['height']:
            break
        rotate_left(0.1)
    while True:
        contour_dict = get_contours_from_frame(get_frame())
        if contour_dict['bottom'][0] >= 0.3 * box_positions['bottom']['width'] * box_positions['bottom']['height']:
            break
        rotate_left(0.1)
 
 
def turn_right():
    move_front_until_clear(True)
    sleep(0.5)
    front(0.3)
    while True:
        contour_dict = get_contours_from_frame(get_frame())
        if contour_dict['right'][0] >= 0.1 * box_positions['right']['width'] * box_positions['right']['height']:
            break
        rotate_right(0.1)
 
    while True:
        contour_dict = get_contours_from_frame(get_frame())
        if contour_dict['bottom'][0] >= 0.3 * box_positions['bottom']['width'] * box_positions['bottom']['height']:
            break
        rotate_right(0.1)
 
 
def adjust_or_move_straight(contour_dict):
    if contour_dict['bottom'][0] >= ADJ_AREA_THRESHOLD * box_positions['bottom']['width'] * box_positions['bottom']['height']:
        # There is path ahead
        top_box_center = np.add(
            (box_positions['bottom']['x'], box_positions['bottom']['y']),
            contour_dict['bottom'][1])
        vector = top_box_center - bot_center
        angle_rad = np.arctan2(vector[1], vector[0])
        angle_deg = np.degrees(angle_rad) + 90
        angle_deg = abs(IMG_WIDTH/2 - top_box_center[0])
 
        # Prioritize adjusting over turning
        if angle_deg > 30 and top_box_center[0] < IMG_WIDTH/2:
            rotate_left(angle_deg/1500)
        elif angle_deg > 30:
            return rotate_right(angle_deg/1500)
        else:
            front(0.1)
    else:
        front(0.1)
 
 
def move_front_until_clear(adj_enabled=False):
    while True:
        contour_dict = get_contours_from_frame(get_frame())
        if adj_enabled:
            adjust_or_move_straight(contour_dict)
        else:
            front(0.1)
        # Move until you clear both left and right path
        if contour_dict['right'][0] <= 0.2 * box_positions['right']['width'] * box_positions['right']['height'] and contour_dict['left'][0] <= 0.2 * box_positions['left']['width'] * box_positions['left']['height']:
            break
 
 
def rotate_right_until_road_found():
    while True:
        contour_dict = get_contours_from_frame(get_frame())
        # Rotate until you are back on the path
        if contour_dict['bottom'][0] >= 0.3 * box_positions['bottom']['width'] * box_positions['bottom']['height']:
            break
        rotate_right(0.1)
 
 
def execute_action(action, angle):
    match action:
        case 'adj_left':
            rotate_left(angle/1500)
        case 'adj_right':
            rotate_right(angle/1500)
        case 'continue':
            front(0.1)
        case 'left':
            turn_left()
        case 'right':
            turn_right()
        case 'leftright':
            turn_left()
        case 'leftstraight':
            front(0.1)
        case 'rightstraight':
            front(0.1)
        case 'leftrightstraight':
            front(0.1)
        case 'deadend':
            rotate_right_until_road_found()
        case _:
            print('No action')
 
 
def get_contours_from_frame(frame):
    thresholded_frame = thresholding(frame)
    segments = generate_segments(thresholded_frame)
    contour_dict = process_segments(segments, thresholded_frame)
    return contour_dict
 
 
def run_path_follower():
    global box_positions
    try:
        box_positions = load_positions_from_file()
        while True:
            frame = get_frame()
            if (frame is None):
                break
 
            ars = detect_aruco_markers(frame)
            if ars != MarkerAction.NONE:
                return ars
 
            action, deg = get_current_road_node(get_contours_from_frame(frame))
            print(action, deg)
 
            if (FRAME_MODE == 1):
                # Camera mode
                execute_action(action, deg)
 
            if (FRAME_MODE == 0):
                # Video mode
                sleep(0.1)
 
            if cv2.waitKey(1) & 0xFF != 255:  # Exit on any key press
                break
 
    except KeyboardInterrupt:
        print('Program terminated')
        stop()
        cv2.destroyAllWindows()
 
 
if __name__ == '__main__':
    try:
        print(run_path_follower())
    except KeyboardInterrupt:
        stop()
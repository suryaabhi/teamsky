### THIS FILE IS USED TO CALIBRATE THE BOX POSITIONS FOR PATH FOLLOWER ###
### YOU WON'T NOT NEED TO DO ANYTHING WITH THIS FILE ###
### SAFE TO IGNORE ###
import cv2
import numpy as np
from time import sleep
from Utils.ImageUtils import get_frame, IMG_WIDTH, IMG_HEIGHT, FRAME_MODE, DEBUG
import json

SEC_BOX_DIMN = 80  # Default dimension for secondary boxes
PRI_BOX_WIDTH = 200  # Uses SEC_BOX_DIMN for Height
NUM_BOXES = 4
COORDINATES_FILE = 'box_positions.json'

# Initialize box positions with dimensions
box_names = ['left', 'right', 'center', 'bottom']
box_positions = {name: {'x': 0, 'y': 0, 'width': SEC_BOX_DIMN,
                        'height': SEC_BOX_DIMN} for name in box_names}


def save_positions_to_file():
    with open(COORDINATES_FILE, 'w') as file:
        json.dump(box_positions, file)


def load_positions_from_file():
    global box_positions
    try:
        with open(COORDINATES_FILE, 'r') as file:
            box_positions = json.load(file)
            return box_positions
    except FileNotFoundError:
        pass


def update_position_x(value, box_name):
    if box_name not in box_positions:
        box_positions[box_name] = {'x': 0, 'y': 0,
                                   'width': SEC_BOX_DIMN, 'height': SEC_BOX_DIMN}
    box_positions[box_name]['x'] = max(
        0, min(value, IMG_WIDTH - box_positions[box_name]['width']))


def update_position_y(value, box_name):
    if box_name not in box_positions:
        box_positions[box_name] = {'x': 0, 'y': 0,
                                   'width': SEC_BOX_DIMN, 'height': SEC_BOX_DIMN}
    box_positions[box_name]['y'] = max(
        0, min(value, IMG_HEIGHT - box_positions[box_name]['height']))


def update_width(value, box_name):
    if box_name not in box_positions:
        box_positions[box_name] = {'x': 0, 'y': 0,
                                   'width': SEC_BOX_DIMN, 'height': SEC_BOX_DIMN}
    box_positions[box_name]['width'] = max(
        1, min(value, IMG_WIDTH - box_positions[box_name]['x']))


def update_height(value, box_name):
    if box_name not in box_positions:
        box_positions[box_name] = {'x': 0, 'y': 0,
                                   'width': SEC_BOX_DIMN, 'height': SEC_BOX_DIMN}
    box_positions[box_name]['height'] = max(
        1, min(value, IMG_HEIGHT - box_positions[box_name]['y']))


def print_box_positions():
    for box_name, pos in box_positions.items():
        print(
            f"{box_name}: x={pos['x']}, y={pos['y']}, width={pos['width']}, height={pos['height']}")


def init():
    load_positions_from_file()
    cv2.namedWindow('Frame')
    cv2.namedWindow('Trackbars')
    cv2.resizeWindow('Trackbars', 400, 1000)

    for box_name in box_names:
        x = box_positions.get(box_name, {}).get('x', 0)
        y = box_positions.get(box_name, {}).get('y', 0)
        width = box_positions.get(box_name, {}).get('width', SEC_BOX_DIMN)
        height = box_positions.get(box_name, {}).get('height', SEC_BOX_DIMN)
        cv2.createTrackbar(f'{box_name} X', 'Trackbars', x, IMG_WIDTH - width,
                           lambda v, box_name=box_name: update_position_x(v, box_name))
        cv2.createTrackbar(f'{box_name} Y', 'Trackbars', y, IMG_HEIGHT - height,
                           lambda v, box_name=box_name: update_position_y(v, box_name))
        cv2.createTrackbar(f'{box_name} W', 'Trackbars', width, IMG_WIDTH,
                           lambda v, box_name=box_name: update_width(v, box_name))
        cv2.createTrackbar(f'{box_name} H', 'Trackbars', height, IMG_HEIGHT,
                           lambda v, box_name=box_name: update_height(v, box_name))


def display_segments(segments):
    for box_name, segment in segments.items():
        if DEBUG:
            cv2.imshow(box_name, cv2.resize(segment,
                                            (box_positions[box_name]['width'], box_positions[box_name]['height'])))


def display_image_with_segments(frame, segments):
    for box_name, segment in segments.items():
        x = box_positions.get(box_name, {}).get('x', 0)
        y = box_positions.get(box_name, {}).get('y', 0)
        width = box_positions.get(box_name, {}).get('width', SEC_BOX_DIMN)
        height = box_positions.get(box_name, {}).get('height', SEC_BOX_DIMN)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (128, 255, 0), 2)
    if DEBUG:
        cv2.imshow('Frame', frame)


def generate_segments(frame):
    segments = {}
    for box_name in box_names:
        x = box_positions.get(box_name, {}).get('x', 0)
        y = box_positions.get(box_name, {}).get('y', 0)
        width = box_positions.get(box_name, {}).get('width', SEC_BOX_DIMN)
        height = box_positions.get(box_name, {}).get('height', SEC_BOX_DIMN)
        segments[box_name] = frame[y:y + height, x:x + width]
    return segments


if __name__ == "__main__":
    init()
    try:
        while True:
            frame = get_frame()
            if frame is None:
                print_box_positions()
                save_positions_to_file()
                break

            segments = generate_segments(frame)
            display_segments(segments)
            display_image_with_segments(frame, segments)
            if (FRAME_MODE == 0):
                sleep(0.1)

            if cv2.waitKey(1) & 0xFF != 255:  # Exit on any key press
                print_box_positions()
                save_positions_to_file()
                break

    except KeyboardInterrupt:
        print("Program terminated")
        print_box_positions()
        save_positions_to_file()

    cv2.destroyAllWindows()

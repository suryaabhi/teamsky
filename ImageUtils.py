import cv2
import numpy as np
from time import sleep

FRAME_MODE = 0  # 0 for video file, 1 for camera input

# Enable this for creating a window to display the frame
# This won't work through VS Code when running on Pi
# For FRAME_MODE 1, you can set True and run directly from laptop
DEBUG = True

MEDIA_INIT = False
FILE_NAME = 'Z0.mp4'
IMG_WIDTH = 640
IMG_HEIGHT = 360


def resize_frame(frame):
    resized_frame = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
    return resized_frame


def get_frame():
    global MEDIA_INIT
    global input_source
    if FRAME_MODE == 0:
        if not MEDIA_INIT:
            input_source = cv2.VideoCapture(FILE_NAME)
            MEDIA_INIT = True
        ret, frame = input_source.read()
        if not ret:
            return None
        frame = resize_frame(frame)
        return frame
    else:
        if not MEDIA_INIT:
            from picamera2 import Picamera2
            # Create a Picamera2 object
            input_source = Picamera2()
            # Get the configuration for video
            camera_config = input_source.create_video_configuration()
            # Configure the camera
            input_source.configure(camera_config)
            # Start the camera
            input_source.start()
            MEDIA_INIT = True
        frame = input_source.capture_array()
        frame = resize_frame(frame)
        return frame


def warp_frame(image):  # Experimental function to warp the frame, not used.
    src1 = [246, 190]
    src2 = [406, 190]
    src3 = [228, 360]
    src4 = [440, 360]

    dst1 = [228, 190]
    dst2 = [440, 190]
    dst3 = [228, 360]
    dst4 = [440, 360]

    if image is None:
        return None

    pts1 = np.float32([src1, src2, src3, src4])
    pts2 = np.float32([dst1, dst2, dst3, dst4])

    # Get the transformation matrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Apply the warp
    warped_image = cv2.warpPerspective(
        image, matrix, (image.shape[1], image.shape[0]))

    return warped_image


if __name__ == '__main__':
    try:
        while True:
            frame = get_frame()
            if frame is None:
                break
            if DEBUG:
                cv2.imshow('Frame', frame)
            else:
                cv2.imwrite("Image_frame.jpg", frame)
            if (FRAME_MODE == 0):
                sleep(0.1)
            if cv2.waitKey(1) & 0xFF != 255:  # Exit on any key press
                break
    except KeyboardInterrupt:
        print('Program terminated')
        cv2.destroyAllWindows()

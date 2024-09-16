from enum import Enum
import cv2
import cv2.aruco as aruco
from BoxPositionsTester import get_frame
from time import sleep
from Utils.ImageUtils import DEBUG


class MarkerAction(Enum):
    NONE = "None"  # Ignore
    READ_BILLBOARD_1 = "Read billboard 1"  # Returns for pick/drop - shape & color
    PICK_OBJECT_LEFT = "Pick object - Left"  # Optionally start search left
    PICK_OBJECT_RIGHT = "Pick object - Right"  # Optionally start search right
    DROP_OBJECT_LEFT = "Drop object - Left"  # Optionally start search left
    DROP_OBJECT_RIGHT = "Drop object - Right"  # Optionally start search right
    READ_BILLBOARD_2 = "Read billboard 2"  # Returns lane to pick
    EXECUTE_LANE = "Execute lane"  # Execute lane from BB2
    READ_BILLBOARD_3 = "Read billboard 3"  # Returns letter to write
    WRITE_LETTER = "Write letter"  # Pick pen and write letter from BB3


# Mapping marker IDs to MarkerAction enum values
marker_action_map = {
    0: MarkerAction.READ_BILLBOARD_1,
    1: MarkerAction.PICK_OBJECT_LEFT,
    2: MarkerAction.PICK_OBJECT_RIGHT,
    3: MarkerAction.DROP_OBJECT_LEFT,
    4: MarkerAction.DROP_OBJECT_RIGHT,
    5: MarkerAction.READ_BILLBOARD_2,
    6: MarkerAction.EXECUTE_LANE,
    7: MarkerAction.READ_BILLBOARD_3,
    8: MarkerAction.WRITE_LETTER
}


def detect_aruco_markers(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    if ids is not None:
        print("Detected ArUco marker IDs:", ids.flatten())
        marker_id = ids.flatten()[0]  # Only use the first detected marker ID
        return marker_action_map.get(marker_id, MarkerAction.NONE)
    else:
        return MarkerAction.NONE


if __name__ == '__main__':
    try:
        while True:
            frame = get_frame()
            if frame is None:
                break
            if DEBUG:
                cv2.imshow('Frame', frame)
            else:
                cv2.imwrite("ARTag_frame.jpg", frame)
            result = detect_aruco_markers(frame)
            print("Result:", result)
            sleep(0.1)
            if cv2.waitKey(1) & 0xFF != 255:  # Exit on any key press
                break
    except KeyboardInterrupt:
        print('Program terminated')
        cv2.destroyAllWindows()

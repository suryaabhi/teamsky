import cv2
import numpy as np
from Utils.ImageUtils import get_frame
import time

def get_centroid(i, image):
    M = cv2.moments(i)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.drawContours(image, [i], -1, (0, 255, 0), 2)
        cv2.circle(image, (cx, cy), 7, (0, 0, 255), -1)
        cv2.putText(image, "center", (cx - 20, cy - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    print(f"cx: {cx} cy: {cy}")
    return cx, cy

def display(image, contour, shape, approx):
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 1)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 10
    cv2.putText(image, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    cv2.imshow('Detected Shapes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_color_shape(image, color, shape):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # rgb -> bgr
    if color == "green":
        color_bgr = np.uint8([[[15,  164, 114]]])
    if color == "red":
        color_bgr = np.uint8([[[181,  41, 37]]])
    if color == "blue":
        color_bgr = np.uint8([[[0,  114, 171]]])
    if color == "orange":
        color_bgr = np.uint8([[[238,  181, 58]]])

    hsv_ = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)
    lower = np.array([hsv_[0][0][0] - 10, 100, 100])
    upper = np.array([hsv_[0][0][0] + 10, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    # cv2.imshow('mask', mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    blurred_mask = cv2.GaussianBlur(mask, (7, 7), 0)
    # cv2.imshow('mask', blurred_mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # smoothed_image = cv2.bitwise_and(image, image, mask=blurred_mask)
   
    contours, _ = cv2.findContours(blurred_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    shape_detected = ""
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 800:
            continue

        approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)
        cx, cy = None, None
        # print(len(approx))

        if len(approx) == 4:
            shape_detected = "square"
            cx, cy = get_centroid(contour, image)
            # display(image, contour, shape_detected, approx)
        elif len(approx) > 13:
            # display(image, contour, shape_detected, approx)
            shape_detected = "circle"
            cx, cy = get_centroid(contour, image)
        if shape == shape_detected:
            print("*********" , color, " " , shape, " shape detected", "*********")
        else:
            print("*********" , color, " " , shape, " shape not detected", "*********")
        if cx is not None and cy is not None:
            delta = 20
            right = 320 + delta
            left = 320 - delta
            if (cx < right) and (cx > left):
                return (True, "center")
            if cx > right:
                return (True, "right")
            elif cx < left:
                return (True, "left")      
    return (False, "")

if __name__ == "__main__":
    while True:
        time.sleep(1)
        image = get_frame()
        ret = detect_color_shape(image, "orange", "circle")
        print("Detected color and shape: ", ret)
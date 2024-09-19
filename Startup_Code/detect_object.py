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
    cv2.putText(image, shape + " contour " + str(len(approx)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    cv2.imshow('Detected Shapes', image)
    cv2.waitKey(1)
    cv2.destroyAllWindows

def detect_color_shape(image, color, shape, delta=20):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # rgb -> bgr
    if color == "green":
        color_bgr = np.uint8([[[33,  159, 87]]])
    if color == "red":
        color_bgr = np.uint8([[[181,  41, 37]]])
    if color == "blue":
        color_bgr = np.uint8([[[3,  48, 106]]])
    
    if color == "blue":
        lower = np.array([max(int(hsv_[0][0][0]) - 15, 0), 140, 60])
        upper = np.array([min(int(hsv_[0][0][0]) + 15, 179), 255, 255])
    if color == "red":
        lower = np.array([max(int(hsv_[0][0][0]) - 15, 0), 135, 60])
        upper = np.array([min(int(hsv_[0][0][0]) + 15, 179), 255, 255])
    if color == "green":
        lower = np.array([max(int(hsv_[0][0][0]) - 15, 0), 135, 40])
        upper = np.array([min(int(hsv_[0][0][0]) + 15, 179), 255, 255])
    hsv_ = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('mask', mask)
    cv2.waitKey(1)
    cv2.destroyAllWindows
    blurred_mask = cv2.GaussianBlur(mask, (7, 7), 0)

    contours, _ = cv2.findContours(blurred_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    shape_detected = ""
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 800:
            continue

        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        cx, cy = None, None
        
        if len(approx) >= 9:
            shape_detected = "circle"
            cx, cy = get_centroid(contour, image)
        elif len(approx) >= 4 and len(approx) <= 8:
            shape_detected = "square"
            cx, cy = get_centroid(contour, image)
        display(image, contour, shape_detected, approx)
        
        if cx is not None and cy is not None and (shape_detected == shape):
            delta = 20
            right = 320 + delta
            left = 320 - delta
            if (cx < right) and (cx > left):
                print("*********" , color, " " , shape, " detected", "in center ",  "*********")
                return (True, "center")
            if cx > right:
                print("*********" , color, " " , shape, " detected", "in right ",  "*********")
                return (True, "right")
            elif cx < left:
                print("*********" , color, " " , shape, " detected", "in left ",  "*********")
                return (True, "left") 

    if __name__ == "__main__":   
        while True:
            image = get_frame()
            # image = cv2.imread("real-world/12.png")
            ret = detect_color_shape(image, "red", "circle")
            # ret = detect_color_shape(image, "red", "square")
            # ret = detect_color_shape(image, "blue", "circle")
            # ret = detect_color_shape(image, "blue", "square")
            # ret = detect_color_shape(image, "green", "circle")
            # ret = detect_color_shape(image, "green", "square")
            # ret = detect_color_shape(image, "orange", "circle")
            print("Detected color and shape: ", ret)       
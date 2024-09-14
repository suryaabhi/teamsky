import cv2
from time import sleep
from ImageUtils import get_frame, FRAME_MODE


def nothing(x):  # Dummy function
    pass


# Create a window and trackbars
cv2.namedWindow('HSV Adjustments')
cv2.createTrackbar('H Min', 'HSV Adjustments', 0, 179, nothing)
cv2.createTrackbar('S Min', 'HSV Adjustments', 0, 255, nothing)
cv2.createTrackbar('V Min', 'HSV Adjustments', 0, 255, nothing)
cv2.createTrackbar('H Max', 'HSV Adjustments', 179, 179, nothing)
cv2.createTrackbar('S Max', 'HSV Adjustments', 255, 255, nothing)
cv2.createTrackbar('V Max', 'HSV Adjustments', 255, 255, nothing)

try:
    while True:
        frame = get_frame()
        if frame is None:
            break

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get current positions of trackbars
        h_min = cv2.getTrackbarPos('H Min', 'HSV Adjustments')
        s_min = cv2.getTrackbarPos('S Min', 'HSV Adjustments')
        v_min = cv2.getTrackbarPos('V Min', 'HSV Adjustments')
        h_max = cv2.getTrackbarPos('H Max', 'HSV Adjustments')
        s_max = cv2.getTrackbarPos('S Max', 'HSV Adjustments')
        v_max = cv2.getTrackbarPos('V Max', 'HSV Adjustments')

        # Define range of HSV values
        lower_hsv = (h_min, s_min, v_min)
        upper_hsv = (h_max, s_max, v_max)

        # Threshold the HSV image to get only desired colors
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

        # Bitwise-AND mask and original image
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Display the resulting frame
        cv2.imshow('Original', frame)
        cv2.imshow('Mask', mask)
        cv2.imshow('Result', result)

        if (FRAME_MODE == 0):
            sleep(0.1)
        if cv2.waitKey(1) & 0xFF != 255:  # Exit on any key press
            break

except KeyboardInterrupt:
    print('Program terminated')
    cv2.destroyAllWindows()

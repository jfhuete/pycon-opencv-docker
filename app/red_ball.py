import cv2
import numpy as np
from time import sleep


def clean_mask(mask):

    # Opening to remove salt and pepper noise

    kernel = np.ones((1, 1), np.uint8)
    mask_opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask_opening


def detection(mask, frame, last_circle):

    MOVE_TRESHOLD = 3

    # Circle detect

    # Find contour in mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    circle = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        try:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        except ZeroDivisionError:
            center = (0, 0)

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # Filter move of circle
            if last_circle:
                diff_x = abs(last_circle['center']['x']-center[0])
                diff_y = abs(last_circle['center']['y']-center[1])
                if diff_x < MOVE_TRESHOLD or diff_y < MOVE_TRESHOLD:
                    x = last_circle['x']
                    y = last_circle['y']
                    radius = last_circle['radius']
                    center = (last_circle['center']['x'],
                              last_circle['center']['y'])
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 0), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            circle = {
                      'x': x,
                      'y': y,
                      'radius': radius,
                      'center': {
                                    'x': center[0],
                                    'y': center[1]
                                }
                      }

    return circle


def main():

    # Video capture
    cap = cv2.VideoCapture(0)

    # Constans with WIDTH and HEIGHT of the screen
    WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # frames per second

    FRAME_RATE = 25

    # HSV color filter values

    H_max = 6.87
    H_min = 0

    S_max = 255
    S_min = 107.1

    V_max = 255
    V_min = 0

    max_hsv_values = np.array([H_max, S_max, V_max], np.uint8)
    min_hsv_values = np.array([H_min, S_min, V_min], np.uint8)

    last_circle = None

    while(True):
        ret, frame = cap.read()

        # Transform the image to HSV color space

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get mask of red ball

        mask = cv2.inRange(frame_hsv, min_hsv_values, max_hsv_values)

        # Clean mask to improve detection

        mask = clean_mask(mask)

        # Detect the ball
        circle = detection(mask, frame, last_circle)

        # Do things ##########################################################

        cv2.line(frame, (int(WIDTH/2), 0), (int(WIDTH/2), int(HEIGHT)),
                 (0, 0, 255), 2)

        # Detect circle position
        if circle and circle['center']['x'] > WIDTH/2:
            cv2.circle(frame, (int(circle['x']), int(circle['y'])),
                       int(circle['radius']), (0, 0, 255), 2)
        ######################################################################

        last_circle = circle

        # Display the resulting frame
        cv2.imshow('frame_hsv', mask)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        sleep(1/FRAME_RATE)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

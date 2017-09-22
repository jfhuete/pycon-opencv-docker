import cv2
import numpy as np
from time import sleep


def clean_mask(mask):

    # Opening to remove salt and pepper noise

    kernel = np.ones((20, 20), np.uint8)
    mask_dilation = cv2.dilate(mask, kernel, iterations=3)
    mask_closing = cv2.morphologyEx(mask_dilation, cv2.MORPH_CLOSE, kernel)

    return mask_closing


def detect(mask):

    # Find contours in the mask and return the boundary rectangle
    i, contours, h = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)

    # Returns contours if exist, if not return None
    if contours:
        return contours[0]
    else:
        return None


def tinto_monitoring(frame, height):
    '''
    This function monitorize how much tinto are in the glass. And activate an
    alarm when you have little tinto
    '''

    # thresold of amount of tinto de verano
    thresold_warning = 230
    thresold_alarm = 160
    thresold_critical = 90

    text_position = (230, 30)

    # Set text according to the amount of tinto de verano
    if height > thresold_warning:
        cv2.putText(frame, "OK", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), thickness=2)
    elif height <= thresold_warning and height > thresold_alarm:
        cv2.putText(frame, "WARNING", text_position, cv2.FONT_HERSHEY_SIMPLEX,
                    1, (55, 175, 212), thickness=2)
    elif height <= thresold_alarm and height > thresold_critical:
        cv2.putText(frame, "ALARM", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), thickness=2)
    elif height <= thresold_critical:
        cv2.putText(frame, "CRITICAL", text_position, cv2.FONT_HERSHEY_SIMPLEX,
                    1, (72, 54, 176), thickness=2)


def main():

    FRAME_RATE = 25

    # Video capture
    cap = cv2.VideoCapture('My_tinto_de_verano.mp4')

    # Constans with WIDTH and HEIGHT of the screen
    WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # HSV color filter values

    H_max = 6.87
    H_min = 0

    S_max = 255
    S_min = 107.1

    V_max = 255
    V_min = 0

    max_hsv_values = np.array([H_max, S_max, V_max], np.uint8)
    min_hsv_values = np.array([H_min, S_min, V_min], np.uint8)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if frame is None:
            break

        # Select a rectangle as roi (empirical)
        v_from = (int(WIDTH/3), 0)
        v_to = (int(WIDTH*2/3), int(HEIGHT))

        # Draw roi
        cv2.rectangle(frame, v_from, v_to, (255, 0, 0), 2)

        # Get roi frame
        roi_frame = frame[0:int(HEIGHT), int(WIDTH/3):int(WIDTH*2/3)]

        # Transform the roi image to HSV color space
        frame_hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

        # Get mask of the tinto de verano

        mask = cv2.inRange(frame_hsv, min_hsv_values, max_hsv_values)

        # Clean mask
        mask = clean_mask(mask)

        # Detect
        contour = detect(mask)

        if contour is not None:
            # Obtain the coordinates of rectangle
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(roi_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            h = 0

        # Do somethings

        tinto_monitoring(frame, h)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.moveWindow("frame", 280, 60)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        sleep(1/FRAME_RATE)

    # When evideo finish, release the capture
    cap.release()
    cv2.destroyAllWindows()

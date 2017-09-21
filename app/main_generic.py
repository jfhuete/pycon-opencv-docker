import cv2
from time import sleep
import numpy as np

cap = cv2.VideoCapture(0)

WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# frames per second

FRAME_RATE = 25

if __name__ == "__main__":
    while(True):
        ret, frame = cap.read()

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        sleep(1/FRAME_RATE)
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    while(True):
        ret, frame = cap.read()

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

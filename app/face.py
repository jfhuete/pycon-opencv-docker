import cv2
import numpy as np
from time import sleep


def main():

    # Video capture
    cap = cv2.VideoCapture(0)

    # Constans with WIDTH and HEIGHT of the screen
    WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # frames per second

    FRAME_RATE = 25

    while(True):
        ret, frame = cap.read()

        # haarcascades path
        haarcascades_path = '/usr/local/share/OpenCV/haarcascades/'

        # Load classifiers

        face_cascade = cv2.CascadeClassifier(
                       haarcascades_path+'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(
                      haarcascades_path+'haarcascade_eye.xml')

        # Detect faces
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)

        for (x, y, w, h) in faces:
            # Draw the face rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            # Get the portion of frame that contains the face
            face_frame = frame[y:y+h, x:x+w]

            # Detect the eyes inside the face_frame
            eyes = eye_cascade.detectMultiScale(face_frame)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face_frame, (ex, ey), (ex+ew, ey+eh),
                              (0, 255, 0), 1)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        sleep(1/FRAME_RATE)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

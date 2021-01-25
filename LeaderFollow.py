import time
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to set
time.sleep(0.1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)::
    cv2.namedWindow("Final", cv2.WINDOW_NORMAL)
    image_taken= frame.array
    # conduct color threshold
    if image_taken:
        (h_frame, w_frame) = image_taken.shape[:2]
        mask=cv2.cvtColor(image_taken, cv2.COLOR_BGR2HSV)
        lower_range=np.array([110,50,50])
        upper_range=np.array([130,255,255])
        image= cv2.inRange(mask,lower_range,upper_range)
        # show the images
        (cnts, _) = cv2.findContours(image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
          # loop over the contours
        for c in cnts:
       # if the contour is too small, ignore it
            if cv2.contourArea(c) < 300:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            deviation_translation=(w_frame/2-(x+w/2))*100/w_frame
            deviation_rotation=(h_frame-w_frame)*100/h_frame
            #put deviations in PID as a sume of deviations
            print("Deviation translation "+str(deviation_translation)+ " Deviation in rotation "+str(deviation_rotation))
            cv2.rectangle(image_taken, (x, y), (x + w, y + h), (0, 0, 255), 2) 
        cv2.imshow("Final",image_taken)
        rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break





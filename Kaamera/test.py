import cv2
import numpy as np
import lembalemba as lmb

lmb.set_cam_settings_from_cli()
cap = cv2.VideoCapture(0)
#lmb.set_cam_settings_from_cli()
ret, frame = cap.read()
cv2.imshow('spycam',frame)
lmb.set_cam_settings_from_cli2()

fieldAreaLimit=[310,100,330,450]
while(True):
        ret, frame = cap.read()
        rows,cols = frame.shape[:2]
        print cols,rows
        cv2.line(frame,(330,rows-1),(330,0),(0,255,0),2)
        cv2.line(frame,(310,rows-1),(310,0),(0,255,0),2)
        
        cv2.line(frame,(cols-1,250),(0,250),(0,255,0),2)
        cv2.line(frame,(cols-1,400),(0,400),(0,255,0),2)
        cv2.cv.fromarray(frame)
        line = cv2.cv.InitLineIterator(cv2.cv.fromarray(frame), (20, 20), (40, 40))
        cv2.rectangle(frame,(fieldAreaLimit[0],fieldAreaLimit[1]),(fieldAreaLimit[2],fieldAreaLimit[3]),(255,0,255),2)
        cv2.imshow('spycam',frame)

        if cv2.waitKey(1) >= 0:
                break

cap.release()

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#cap2 = cv2.VideoCapture(1)

lower_values = np.array((79,98,101))
upper_values = np.array((101,191,158))

while(True):
        ret, frame = cap.read()

        frame = cv2.blur(frame,(3,3))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_values, upper_values) #thresholding using hsv values

        kernel = np.ones((5,5),np.uint8) #erosion and dilation size

        #erosion = cv2.erode(mask,kernel,iterations = 1)
        #dilation = cv2.dilate(erosion,kernel,iterations = 1)

        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) #opening erodes and then dialates the image

        fast = cv2.FastFeatureDetector()# Initiate FAST object with default values
        # find and draw the keypoints
        kp = fast.detect(opening,None)
        objects = cv2.drawKeypoints(opening, kp, color=(255,0,0))

        '''
        surf = cv2.SURF(80000) #using surf to detect the object
        surf.upright = True
        kp, des = surf.detectAndCompute(opening,None)
        print(des.shape)
        objects = cv2.drawKeypoints(frame,kp,None,(255,0,0),4)
        if kp != []:
                kp.sort()
                [x,y]=kp[0].pt
                print([x,y])
                cv2.circle(objects,(int(x),int(y)),10,(255,0,0),-1)
        '''

        #res = cv2.bitwise_and(frame,frame, mask= mask)

        #cv2.imshow('mask',mask)
        #cv2.imshow('opening',opening)
        cv2.imshow('objects',objects)

        #cv2.imshow('res',res)
        #ret, frame2 = cap2.read()
        #cv2.imshow('frame', frame)
        #cv2.imshow('frame2', frame2)

        if cv2.waitKey(1) >= 0:
                break


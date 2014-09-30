import cv2
import numpy as np
import copy
##from matplotlib import pyplot as plt


def pixelfind(x,y,color):
    value = copy.deepcopy(frame[y][x])
    ##print value
    frame[y][x]=color
	
    for i in range (10):
        for j in range (10):
            if j==0 or j==9 or i==0 or i==9:
                frame[y-j][x-i]=color
    return value

cap = cv2.VideoCapture(1)

rectcolor = [0,0,255]
while(True):
    ret, frame = cap.read()
    value=pixelfind(320,240,rectcolor)
##    pixelfind(240,320,[0,0,255])
    ##print value
    if value[2]>100 and value[1]<(value[2]/2) and value[0]<(value[2]/2):
        ##print "RED"
        rectcolor=[0,255,0]
    else:
        rectcolor=[0,0,255]
        
    
        

##	ret,thresh1 = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
##	ret,thresh1 = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
##        ret,thresh2 = cv2.threshold(frame,127,255,cv2.THRESH_BINARY_INV)
##        ret,thresh3 = cv2.threshold(frame,127,255,cv2.THRESH_TRUNC)
##        ret,thresh4 = cv2.threshold(frame,127,255,cv2.THRESH_TOZERO)
##        ret,thresh5 = cv2.threshold(frame,127,255,cv2.THRESH_TOZERO_INV)


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) >= 0:
      break


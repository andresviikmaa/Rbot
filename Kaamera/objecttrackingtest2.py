import cv2
import numpy as np
import copy
##from matplotlib import pyplot as plt
from Tkinter import *

master = Tk()
w1 = Scale(master, from_=110, to=255, orient=HORIZONTAL)
w1.pack()
w2 = Scale(master, from_=50, to=255, orient=HORIZONTAL)
w2.pack()
w3 = Scale(master, from_=50, to=255, orient=HORIZONTAL)
w3.pack()
w4 = Scale(master, from_=130, to=255, orient=HORIZONTAL)
w4.pack()
w5 = Scale(master, from_=255, to=255, orient=HORIZONTAL)
w5.pack()
w6 = Scale(master, from_=255, to=255, orient=HORIZONTAL)
w6.pack()

##w1.get()
##w2.get()
##w3.get()
##w4.get()
##w5.get()
##w6.get()

cap = cv2.VideoCapture(0)

rectcolor = [0,0,255]
while(True):
    ret, frame = cap.read()
    
    lower_values = np.array((w1.get(),w2.get(),w3.get()))
    upper_values = np.array((w4.get(),w5.get(),w6.get()))
    
    # smooth it
    frame = cv2.blur(frame,(3,3))

    # convert to hsv and find range of colors
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #thresh = cv2.inRange(hsv,np.array((0, 80, 80)), np.array((20, 255, 255)))
    #thresh2 = thresh.copy()

    #mask
    mask = cv2.inRange(hsv, lower_values, upper_values)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    
        
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    
    if cv2.waitKey(1) >= 0:
      break

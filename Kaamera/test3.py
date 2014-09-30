import cv2
import numpy as np

trsV=[]
def openfile():
    f=open("save.txt","r")
    line=f.readline().split()
    for i,val in enumerate(line):
        trsV.append(int(val))


def findblob(frame,cnt):
    area = cv2.contourArea(cnt)
    #print area
    #perimeter = cv2.arcLength(cnt,True)
    #print perimeter
    #hull = cv2.convexHull(cnt)
    #print hull
    M = cv2.moments(cnt)

    
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print str(cx)+" : "+str(cy)
    cv2.circle(frame,(cx,cy),int(area**0.5),(255,0,0),3)
    
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    #rect = cv2.minAreaRect(cnt)
    #box = cv2.boxPoints(rect)
    #box = np.int0(box)
    #cv2.drawContours(frame,[box],0,(0,0,255),2)


cap = cv2.VideoCapture(0)
#cap2 = cv2.VideoCapture(1)

openfile()
lower_values = np.array((trsV[0],trsV[1],trsV[2]))
upper_values = np.array((trsV[3],trsV[4],trsV[5]))

while(True):
        ret, frame = cap.read()
        frame = cv2.blur(frame,(3,3))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_values, upper_values) #thresholding using hsv values
        kernel = np.ones((5,5),np.uint8) #erosion and dilation size

        #erosion = cv2.erode(mask,kernel,iterations = 1)
        #dilation = cv2.dilate(erosion,kernel,iterations = 1)

        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) #opening erodes and then dialates the image

        #imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(opening,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        
        if contours !=[]:
            cv2.drawContours(frame, contours, -1, (0,255,0), 3)
            areas=[]
            
            '''
            for i in contours:
                areas.append(cv2.contourArea(i))
            '''
            
            maximum=0
            for i,cntur in enumerate(contours):
                value=cv2.contourArea(cntur)
                if value>maximum:
                    maximum=value
                    index=i
            cnt = contours[index]
 
            findblob(frame,cnt)


            #cnt = contours[0]
##            area = cv2.contourArea(cnt)
##            #print area
##            perimeter = cv2.arcLength(cnt,True)
##            #print perimeter
##            hull = cv2.convexHull(cnt)
##            #print hull
##            M = cv2.moments(cnt)
##
##            
##            cx = int(M['m10']/M['m00'])
##            cy = int(M['m01']/M['m00'])
##            print str(cx)+" : "+str(cy)
##            cv2.circle(frame,(cx,cy),10,(255,0,0),-1)
##            
##            x,y,w,h = cv2.boundingRect(cnt)
##            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
##            #rect = cv2.minAreaRect(cnt)
##            #box = cv2.boxPoints(rect)
##            #box = np.int0(box)
##            #cv2.drawContours(frame,[box],0,(0,0,255),2)
            
        #cv2.imshow('f', cnt)
        #res = cv2.bitwise_and(frame,frame, mask= mask)

        #cv2.imshow('mask',mask)
        #cv2.imshow('opening',opening)
        #cv2.imshow('thresh',thresh)
        #cv2.imshow('objects',objects)

        #cv2.imshow('res',res)
        #ret, frame2 = cap2.read()
        cv2.imshow('frame2', frame)
        #cv2.imshow('frame2', frame2)

        if cv2.waitKey(1) >= 0:
                break



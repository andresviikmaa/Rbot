import cv2
import numpy as np
trsV=[]
def openFile():
    f=open("save.txt","r")
    for line in f:
        Linevalues=[]
        line=line.split()
        for i,val in enumerate(line):
            Linevalues.append(int(val))
        if Linevalues==[]:
            print "No line values read error."
            Linevalues=[0,0,0,255,255,255]
        else:
            print "Line values loaded."
        trsV.append(Linevalues)

def setThresholds(trsV):
    lower_values = np.array((trsV[0],trsV[1],trsV[2]))
    upper_values = np.array((trsV[3],trsV[4],trsV[5]))
    return [lower_values,upper_values]

def beginCapture():
    global cap,ballTV,fieldTV,goalTV,blackTV,whiteTV,xyLocation,fieldAreaLimit
    xyLocation=[[],[],[],[],[]]
    fieldAreaLimit=[100,100,200,200]
    cap = cv2.VideoCapture(0)
    openFile()
    ballTV=setThresholds(trsV[0])
    fieldTV=setThresholds(trsV[1])
    goalTV=setThresholds(trsV[2])
    blackTV=setThresholds(trsV[3])
    whiteTV=setThresholds(trsV[4])

def findObject(frame,cnt):
    area = cv2.contourArea(cnt)
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    #---#frame indicators:
    cv2.circle(frame,(cx,cy),int(area**0.5),(255,0,0),3) #----# DISPLAYS OBJECT CENTER
    #x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    
    return [cx,cy,area]

def findLine(frame,cnt):
    rows,cols = frame.shape[:2]
    [vx,vy,x,y] = cv2.fitLine(cnt, cv2.cv.CV_DIST_L2,0,0.01,0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((cols-x)*vy/vx)+y)
    cv2.line(frame,(cols-1,righty),(0,lefty),(0,255,0),2)#----# DISPLAYS LINE
    
    return [(cols-1,righty),(0,lefty)]

def findArea(frame,cnt):
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    cv2.rectangle(frame,(fieldAreaLimit[0],fieldAreaLimit[1]),(fieldAreaLimit[2],fieldAreaLimit[3]),(255,0,255),2)
    if defects!=None:
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            far = tuple(cnt[f][0])
            if far[0]<fieldAreaLimit[0] or far[0]>fieldAreaLimit[2] or far[1]<fieldAreaLimit[1] or far[1]>fieldAreaLimit[3]:
                cv2.circle(frame,far,5,[0,255,0],-1)#----# SHOWS INNER CIRCLES
                #return False
            else:
                cv2.circle(frame,far,5,[0,0,255],-1)#----# SHOWS INNER CIRCLES
                return False
    return True


def tracking(treshold,Ttype,count):
    mask = cv2.inRange(hsv, treshold[0], treshold[1]) #thresholding using hsv values
    if Ttype=="area":
        kernel = np.ones((10,10),np.uint8) #erosion and dilation size for area recognition
    else:
        kernel = np.ones((5,5),np.uint8) #erosion and dilation size
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) #opening erodes and then dialates the image
    ret,thresh = cv2.threshold(opening,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('frame2', mask)
    if contours !=[]:
            #cv2.drawContours(frame, contours, -1, (0,255,0), 3) #---# draws the countours
            outputValues=[]
            
            '''
            for i in contours:
                areas.append(cv2.contourArea(i))
            '''
            
            maximum=0
            index=0
            for i,cntur in enumerate(contours):
                value=cv2.contourArea(cntur)
                if value>maximum:
                    maximum=value
                    index2=index
                    index=i
            cnt = contours[index]
            if count==2:
                outputValues.append(findObject(frame,contours[index2]))


                
            if Ttype=="object":
                outputValues.append(findObject(frame,cnt))
            elif Ttype=="line":
                outputValues.append(findLine(frame,cnt))
            elif Ttype=="area":
                outputValues.append(findArea(frame,cnt))
            return outputValues

    
def canShoot(fieldClear,hasBall,goalPos):
    if fieldClear==True and hasBall:
        if goalPos[0][0]<screenCenter-10 and goalPos[1][0]>screenCenter+10:
            return True
    return False

def visionFocus(hasBall):
    if hasBall:
        xyLocation[1]=tracking(fieldTV,"area",1)
        xyLocation[2]=tracking(goalTV,"object",2)
        if canShoot(xyLocation[1],hasBall,xyLocation[2]):
            #----SHOOT BALL----#
            print "Shot"
    else:
        xyLocation[0]=tracking(ballTV,"object",1)
    xyLocation[3]=tracking(blackTV,"line",1)
    xyLocation[4]=tracking(whiteTV,"line",1)

    

def frameProcessing():
    global ret,frame,hsv
    ret, frame = cap.read()
    frame = cv2.blur(frame,(3,3))
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    xyLocation[0]=tracking(ballTV,"object",1)
    #xyLocation[1]=tracking(fieldTV,"area",1)
    #xyLocation[2]=tracking(goalTV,"object")
    #xyLocation[3]=tracking(blackTV,"line")
    #xyLocation[4]=tracking(whiteTV,"line")
    #print xyLocation


    




    
    cv2.imshow('frame', frame)



def initCam():
    beginCapture()
    while(True):
        frameProcessing()
        
        if cv2.waitKey(1) >= 0:
                cap.release()
                cv2.destroyAllWindows()
                break
#initCam()



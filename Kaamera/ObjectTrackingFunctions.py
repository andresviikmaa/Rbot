import cv2
import numpy as np
import lembalemba as lmb



trsV=[]
outputless=False
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
    global cap,ballTV,fieldTV,goal1TV,goal2TV,blackTV,whiteTV,xyLocation,fieldAreaLimit
    
    xyLocation=[[],[],[],[],[]]
    fieldAreaLimit=[310,100,330,450] #<clear field size

    lmb.set_cam_settings_from_cli()
    
    
    
    cap = cv2.VideoCapture(0)
    openFile()
    ballTV=setThresholds(trsV[0])
    fieldTV=setThresholds(trsV[1])
    goal1TV=setThresholds(trsV[2])
    goal2TV=setThresholds(trsV[3])
    blackTV=setThresholds(trsV[4])
    whiteTV=setThresholds(trsV[5])

    for i in range(10):
        frameProcessing(False,1)
        if cv2.waitKey(1) >= 0:
                break
    lmb.set_cam_settings_from_cli2()

def findObject(frame,cnt):
    area = cv2.contourArea(cnt)
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    #---#frame indicators:
    if not outputless:
        cv2.circle(frame,(cx,cy),int(area**0.5),(255,0,0),3) #----# DISPLAYS OBJECT CENTER
    #x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    
    return [cx,cy,area]

def findGoal(frame,cnt):
    #area = cv2.contourArea(cnt)
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    #---#frame indicators:
    #cv2.circle(frame,(cx,cy),int(area**0.5),(255,0,0),3) #----# DISPLAYS OBJECT CENTER
    x,y,w,h = cv2.boundingRect(cnt)
    if not outputless:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    fieldAreaLimit[1]=y+h+20

    
    return [cx,cy,w]

def findToLine(frame,mask,pos):
    [x,y,none]=pos

    rows,cols = frame.shape[:2]
    
    line = cv2.cv.InitLineIterator(cv2.cv.fromarray(mask), ((cols-1)/2, rows-1), (x, y))
    if not outputless:
        cv2.line(frame,(((cols-1)/2), rows-1),(x, y),(0,255,0),2)#----# DISPLAYS LINE

    #mask = cvCreateMat(480, 640, CV_8UC1)
    #rows,cols = frame.shape[:2]
    #[vx,vy,x,y] = cv2.fitLine(cnt, cv2.cv.CV_DIST_L2,0,0.01,0.01)
    #lefty = int((-x*vy/vx) + y)
    #righty = int(((cols-x)*vy/vx)+y)
    #buffer=[]
    for i in line:
        #buffer.append(i)
        #if len(buffer)>1:
        #    buffer.pop(0)
        #print buffer[0]

        
        #if buffer[0]==255:
            #print buffer[0]
        #    if buffer[-1]==255:
        if i==255:
            if not outputless:
                cv2.line(frame,(20, 20),(20, 30),(0,255,0),2)
            return True
    if not outputless:
        cv2.line(frame,(20, 20),(20, 30),(255,0,0),2)
            
        #cv2.line(frame,(i[0],i[1]),(i[0],i[1]),(0,255,0),2)#----# DISPLAYS LINE
    #cv2.line(frame,(((cols-1)/2), rows-1),(x, y),(0,255,0),2)#----# DISPLAYS LINE
    #cv2.line(frame,(20, 20),(20, 30),aby,2)
    
    return False

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


def tracking(treshold,Ttype,tracker):
    mask = cv2.inRange(hsv, treshold[0], treshold[1]) #thresholding using hsv values
    if Ttype=="area":
        kernel = np.ones((10,10),np.uint8) #erosion and dilation size for area recognition
    else:
        kernel = np.ones((5,5),np.uint8) #erosion and dilation size
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) #opening erodes and then dialates the image
    ret,thresh = cv2.threshold(opening,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow('frame2', mask)
    if contours !=[]:
            #cv2.drawContours(frame, contours, -1, (0,255,0), 3) #---# draws the countours
            outputValues=[]
            
            '''
            for i in contours:
                areas.append(cv2.contourArea(i))
            '''
            
            maximum=0
            #index=0
            
            for i,cntur in enumerate(contours):
                value=cv2.contourArea(cntur)
                if value>maximum:
                    maximum=value
                    #index2=index
                    index=i
            cnt = contours[index]
            #if count==2:
            #    outputValues.append(findObject(frame,contours[index2]))


            if Ttype=="object1":
                outputValues.append(findObject(frame,cnt))
            #elif Ttype=="object2":
            #    outputValues.append(findObject(frame,contours[index2]))
            elif Ttype=="goal":
                outputValues.append(findGoal(frame,cnt))
            elif Ttype=="line":
                #outputValues.append(findLine(frame,cnt))
                outputValues.append(findToLine(frame,mask,tracker))
            elif Ttype=="area":
                outputValues.append(findArea(frame,cnt))
            return outputValues

    
def canShoot(fieldClear,hasBall,goalPos):
    if fieldClear==True and hasBall:
        if goalPos[0][0]<screenCenter-10 and goalPos[1][0]>screenCenter+10:
            return True
    return False

def visionFocus(hasBall,goalType):
    if hasBall:
        #xyLocation[1]=tracking(fieldTV,"area",0)
        xyLocation[1]=[True]
        if goalType==1:
            xyLocation[2]=tracking(goal1TV,"goal",0)
        elif goalType==2:
            xyLocation[2]=tracking(goal2TV,"goal",0)


    else:
        
        xyLocation[0]=tracking(ballTV,"object1",0)
        if xyLocation[0]!=None and False:
            Isblackline=tracking(blackTV,"line",xyLocation[0][0])
            if Isblackline!=None:
                if Isblackline[0]:
                    xyLocation[0]=[[0,0,0]]
                
                #print "line!"
                #xyLocation[0]=tracking(ballTV,"object2",0)
                #if tracking(blackTV,"line",xyLocation[0][0]):
                #    print "line2"
                #    xyLocation[0]=None
        
        
    #xyLocation[3]=tracking(blackTV,"line")
    #xyLocation[4]=tracking(whiteTV,"line")

##beginCapture()
##visionFocus(False,1)
    

def frameProcessing(hasBall,goalType):
    global ret,frame,hsv
    ret, frame = cap.read()
    frame = cv2.blur(frame,(3,3))
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    visionFocus(hasBall,goalType)

    #xyLocation[0]=tracking(ballTV,"object")
    #xyLocation[1]=tracking(fieldTV,"area")
    #xyLocation[2]=tracking(goalTV,"goal")
    #xyLocation[3]=tracking(blackTV,"line")
    #xyLocation[4]=tracking(whiteTV,"line")
    #print xyLocation


    




    #if not outputless:
    cv2.imshow('frame', frame)



def initCam():
    beginCapture()
    while(True):
        frameProcessing()
        print xyLocation
        
        if cv2.waitKey(1) >= 0:
                cap.release()
                cv2.destroyAllWindows()
                break
#initCam()



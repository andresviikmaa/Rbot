import Kaamera.ObjectTrackingFunctions as Camera
import Servo.ManoeuveringFunctions as Servos
import Logic.GameplayLogic as Logic
import Coilgun.CoilgunFunctions as Coil
import time
#hasBall=False
hasBall=True #<permagoal
Servos.maxrotorvalue=32
TimeoutTimer=0
ShootSetupTimer=0
TargetLocated=[False,1,1]


AimAtGoal=1 #goals are 1 and 2

outputless=False
#outputless=True

if outputless:
    Camera.outputless=True
    Servos.outputless=True
print Servos.GlobalStop


#Logic.ObjectGoto([299, 153, 276.0])

try:
    Servos.findMotor(0)
    Servos.setup(61,62,63)
    Coil.CoilSetup(3)
except:
    print "Servo setup failed"

try:
    Camera.beginCapture()
    #for i in range(200):
    #    Camera.frameProcessing(False,AimAtGoal)
except:
    print "Camera setup failed."

try:
    input()
except:
    print "begin"
try:
    Servos.maxrotorvalue=60
    #Servos.move([Servos.maxrotorvalue,0,0])
    #time.sleep(1)
except:
    print "move failure"

#try:
if True:

    #try:
    #    Camera.beginCapture()
    #except:
    #    print "Camera setup failed."
    while(TimeoutTimer<500 and not Servos.GlobalStop):
        if TimeoutTimer>400:
            Servos.maxrotorvalue=120
            Servos.move([Servos.maxrotorvalue,0,0])
            time.sleep(1)
            TimeoutTimer=0

        hasBall=Servos.readLED()
        Camera.frameProcessing(hasBall,AimAtGoal)
        #print Camera.xyLocation
        #try:
        #    Coil.Ping()
        #except:
        #    print "fugger failure"
        #if True:
        try:
            if hasBall:
            #if Servos.readLED():
                #hasball=True
                Servos.maxrotorvalue=60
                if Camera.xyLocation[2]!=None and Camera.xyLocation[1]!=None:
                    Servos.maxrotorvalue=30
                    TimeoutTimer=0
                    try:
                        #print Camera.xyLocation[2],Camera.xyLocation[1]
                        Servos.move(Logic.TurnTo(Camera.xyLocation[2][0],Camera.xyLocation[1][0]))
                    except:
                        Servos.move([Servos.maxrotorvalue/2.0,0,Servos.maxrotorvalue/2.0])
                        Logic.Canshoot=False
                        print "cameraproblem"
                    if Logic.Canshoot:
                        
                        if ShootSetupTimer<14:
                            ShootSetupTimer+=1
                            
                        else:
                            Servos.move([0,0,0])
                            ShootSetupTimer=0
                            try:
                                Coil.Dribbler(False)
                                time.sleep(0.2)
                                Coil.Shoot(10000)
                            except:
                                print "dribbler failure"
                                try:
                                    Coil.Dribbler(False)
                                    time.sleep(0.4)
                                    Coil.Shoot(10000)
                                except:
                                    print "dribbler abort"
                            
##                            for i in range(10): #The kicking part happens here(it's a test)
##                                if simulation:
##                                    Vmove.move([255*2,0,0])
##                                    print [255*2,0,0]
##                                else:
##                                    Servos.maxrotorvalue=50
##                                    Servos.move([50,0,0])
##                                    Servos.maxrotorvalue=19
##                                time.sleep(0.1)
                            #ShootSetupTimer=0
                            for i in range(5):
                                Servos.move([0,0,Servos.maxrotorvalue])
                                time.sleep(0.1)

                            
                            #hasBall=False
                            TargetLocated[2]=1
                        #hasBall=True #<permagoal
                    TimeoutTimer=0
                else:
                    #if TimeoutTimer%30<26: #<stopper when turning
                    if TimeoutTimer%40<36:
                        Servos.move([Servos.maxrotorvalue,-90,-Servos.maxrotorvalue])
                    else:
                        Servos.move([0,0,0])
                    TimeoutTimer+=1
            else:
                Servos.maxrotorvalue=60
                if Camera.xyLocation[0]!=None:
                    TimeoutTimer=0
                    try:
                        Servos.move(Logic.ObjectGoto(Camera.xyLocation[0][0]))
                    except:
                        Servos.move([Servos.maxrotorvalue/2.0,0,Servos.maxrotorvalue/2.0])
                        print "cameraproblem2"
                    if Camera.xyLocation[0][0][1]>200: #dribbler turns on
                        Servos.maxrotorvalue=30
                        #Servos.maxrotorvalue=16
                        #hasBall=True

                        
                        try:
                            Coil.Dribbler(True)
                            #print "dribbler active"
                        except:
                            print "dribbler failure, retry"
                            #try:
                            #    Coil.Dribbler(True)
                                
                            #except:
                            #    print "dribbler abort"
                        if Camera.xyLocation[0][0][1]>400 and Camera.xyLocation[0][0][0]<350 and Camera.xyLocation[0][0][0]>290: #Part where it recognises it has the ball
                            #hasBall=True
                            Servos.move([Servos.maxrotorvalue,0,0])
                            time.sleep(0.1)
                        #hasBall=False #<permaball
                    TimeoutTimer=0

                    TargetLocated[0]=True
                else:
                    #if TimeoutTimer%30<26: #<stopper when turning
                    if TargetLocated[0]:
                        TargetLocated=[False,TargetLocated[1]*-1,TargetLocated[2]]
                        TargetLocated[2]+=1
                        if TargetLocated[2]>3:
                            TargetLocated[2]=2

                        
                    turnspeed=Servos.maxrotorvalue/(float(TargetLocated[2])*TargetLocated[1])/(1+float((TimeoutTimer+1)/50.0))
                    if turnspeed<5:
                        turnspeed=5
                    Servos.move([0,0,turnspeed])
                    print turnspeed,(1+float((TimeoutTimer+1)/50.0))
##                    if TimeoutTimer%30<25:
##                        Servos.move([0,0,Servos.maxrotorvalue])Servos.move([0,0,Servos.maxrotorvalue/float(TargetLocated[2])*TargetLocated[1]])
##                    else:
##                        Servos.move([0,0,0])
                    TimeoutTimer+=1
        except:
            print "Functional error."
        #print str(Camera.xyLocation[0][0])

        if Camera.cv2.waitKey(1) >= 0:
                Servos.move([0,0,0])
                Camera.cap.release()
                Camera.cv2.destroyAllWindows()
                break

    try:
        Servos.move([0,0,0])
        Servos.closeConnections()
        Camera.cap.release()
        Camera.cv2.destroyAllWindows()
        Coil.closeConnection()
    except:
        print "Timed out becuase the tracked object isn't visible."
##except:
##    print "Session aborted."
try:
    Coil.closeConnection()
    print "coil shutdown"
except:
    print "coil shutdown failure"
try:
    Servos.move([0,0,0])
    Servos.closeConnections()
    print "servo shutdown"
except:
    print "servo shutdown failure"
try:
        Camera.cap.release()
        Camera.cv2.destroyAllWindows()
        print "Had to use special shutdown."
except:
        print "Basic shutdown worked."

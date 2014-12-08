import Kaamera.ObjectTrackingFunctions as Camera
import Servo.ManoeuveringFunctions as Servos
import Logic.GameplayLogic as Logic
import Coilgun.CoilgunFunctions as Coil
import time
hasBall=False
#hasBall=True #<permagoal
Servos.maxrotorvalue=32
TimeoutTimer=0
ShootSetupTimer=0
print Servos.GlobalStop
simulation=True
simulation=False
if simulation:
    import Visualizationofmovement as Vmove
    Vmove.move([0,0,0])

#Logic.ObjectGoto([299, 153, 276.0])
if not simulation:
    try:
        Servos.findMotor(0)
        Servos.setup(61,62,63)
        Coil.CoilSetup(3)
    except:
        print "Servo setup failed"

try:
#if True:
    try:
        Camera.beginCapture()
    except:
        print "Camera setup failed."
    while(TimeoutTimer<500 and not Servos.GlobalStop):
        Camera.frameProcessing(hasBall,1)
        Coil.Ping()
        #if True:
        try:
            if hasBall:
                Servos.maxrotorvalue=19
                if Camera.xyLocation[2]!=None:
                    if simulation:
                        Vmove.move(Logic.TurnTo(Camera.xyLocation[2][0],Camera.xyLocation[1][0]))
                        print Logic.TurnTo(Camera.xyLocation[2][0],Camera.xyLocation[1][0])
                    else:
                        Servos.move(Logic.TurnTo(Camera.xyLocation[2][0],Camera.xyLocation[1][0]))
                    if Logic.Canshoot:
                        
                        if ShootSetupTimer<10:
                            ShootSetupTimer+=1
                        else:
                            Coil.Shoot(1000)
                            Coil.Dribbler(False)
                            
##                            for i in range(10): #The kicking part happens here(it's a test)
##                                if simulation:
##                                    Vmove.move([255*2,0,0])
##                                    print [255*2,0,0]
##                                else:
##                                    Servos.maxrotorvalue=50
##                                    Servos.move([50,0,0])
##                                    Servos.maxrotorvalue=19
##                                time.sleep(0.1)
                            ShootSetupTimer=0
                            for i in range(10):
                                Servos.move([Servos.maxrotorvalue,180,0])

                            
                            hasBall=False
                        #hasBall=True #<permagoal
                    TimeoutTimer=0
                else:
                    #if TimeoutTimer%30<26: #<stopper when turning
                    if TimeoutTimer%40<36:
                        if simulation:
                            Vmove.move([0,0,255])
                            print [0,0,255]
                        else:
                            Servos.move([Servos.maxrotorvalue,90,Servos.maxrotorvalue])
                    else:
                        if simulation:
                            Vmove.move([0,0,0])
                            print [0,0,0]
                        else:
                            Servos.move([0,0,0])
                    TimeoutTimer+=1
            else:
                Servos.maxrotorvalue=38
                if Camera.xyLocation[0]!=None:
                    if simulation:
                        Vmove.move(Logic.ObjectGoto(Camera.xyLocation[0][0]))
                        print Logic.ObjectGoto(Camera.xyLocation[0][0])
                    else:
                        Servos.move(Logic.ObjectGoto(Camera.xyLocation[0][0]))
                    if Camera.xyLocation[0][0][1]>400: #dribbler turns on
                        Coil.Dribbler(True)
                        if Camera.xyLocation[0][0][1]>450: #Part where it recognises it has the ball
                            hasBall=True
                        #hasBall=False #<permaball
                    TimeoutTimer=0
                else:
                    #if TimeoutTimer%30<26: #<stopper when turning
                    if TimeoutTimer%10<6:
                        if simulation:
                            Vmove.move([0,0,255])
                            print [0,0,255]
                        else:
                            Servos.move([0,0,Servos.maxrotorvalue])
                    else:
                        if simulation:
                            Vmove.move([0,0,0])
                            print [0,0,0]
                        else:
                            Servos.move([0,0,0])
                    TimeoutTimer+=1
        except:
            print "Functional error."
        #print str(Camera.xyLocation[0][0])
        if Camera.cv2.waitKey(1) >= 0:
                Servos.move([0,0,0])
                Servos.closeConnections()
                Camera.cap.release()
                Camera.cv2.destroyAllWindows()
                Coil.closeConnection()
                break
    try:
        Servos.move([0,0,0])
        Servos.closeConnections()
        Camera.cap.release()
        Camera.cv2.destroyAllWindows()
        Coil.closeConnection()
    except:
        print "Timed out becuase the tracked object isn't visible."
except:
    print "Session aborted."
try:
        Camera.cap.release()
        Camera.cv2.destroyAllWindows()
        print "Had to use special shutdown."
except:
        print "Basic shutdown worked."

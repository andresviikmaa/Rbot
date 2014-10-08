import Kaamera.ObjectTrackingFunctions as Camera
import Servo.ManoeuveringFunctions as Servos
import Logic.GameplayLogic as Logic



#Logic.ObjectGoto([299, 153, 276.0])
try:
    0/0
    Servos.setup(1,2,3)
except:
    print "Servo setup failed"

try:
    try:
        Camera.beginCapture()
    except:
        print "Camera setup failed."
    while(True):
        Camera.frameProcessing()
        try:
            if Camera.xyLocation[0]!=None:
                print Logic.ObjectGoto(Camera.xyLocation[0][0])
        except:
            print "Functional error."
        #print str(Camera.xyLocation[0][0])
        if Camera.cv2.waitKey(1) >= 0:
                Camera.cap.release()
                Camera.cv2.destroyAllWindows()
                break
except:
    print "Session aborted."

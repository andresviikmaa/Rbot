import ObjectTrackingFunctions as Camera



#try:
#    try:
Camera.beginCapture()
 #   except:
 #       print "setup failure"        
while(True):
 #       try:
    Camera.frameProcessing(False,3)
 #       except:
 #           print "camera error"

    if Camera.cv2.waitKey(1) >= 0:
                Camera.cap.release()
                Camera.cv2.destroyAllWindows()
                break
#except:
#        Camera.cap.release()
#        Camera.cv2.destroyAllWindows()
        
Camera.cap.release()
Camera.cv2.destroyAllWindows()

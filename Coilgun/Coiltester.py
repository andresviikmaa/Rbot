import CoilgunFunctions as Coil
import time

coilID=3
try:
    Coil.CoilSetup(coilID)
    for i in range(1):
        Coil.Dribbler(True)
        time.sleep(25)
        Coil.Dribbler(False)
        #time.sleep(0.2*(i+1))
        #Coil.Shoot(10000)
        Coil.Dribbler(False)
        #time.sleep(1)

##    for i in range(5):
##        time.sleep(1)
##        Coil.Ping()
##        if i%2==1:
##            Coil.Dribbler(False)
##        else:
##            Coil.Dribbler(True)

    #for i in range(2):
    #    time.sleep(0.5)
    #    Coil.Ping()
    #Coil.Shoot(1000)
    
except:
    print "Session aborted."

try:
    Coil.closeConnection()
except:
    print "Session close failed."

import Servo.ManoeuveringFunctions as Servos
try:
    Servos.findMotor(0)
    Servos.setup(61,62,63)
except:
    print "Servo setup failed"

for i in range(10000): 
    print(Servos.readLED())
try:
    Servos.move([0,0,0])
    Servos.closeConnections()
except:
    print "end"

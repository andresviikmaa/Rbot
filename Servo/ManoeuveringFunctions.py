import serial
import math
import time
servoID1,servoID2,servoID3=0,0,0 #servo ID numbers
deg1,deg2,deg3=0,0,0 #rotor positions on the machine
maxrotorvalue=0; #max speed the rotor can achieve
COMerror=False #in case a rotor COM is not found

GlobalStop=False
removeString="<s:>"

def readMove(inputVal,inputString):
    for i in removeString:
        s =s.replace(i,"")
    if int(s)<inputVal/2:
        GlobalStop=True

def move(speed,direction,rotate,rspeed):#speed is movespeed, rspeed is rotational speed, rotate signifies the direction of rotation
    tspeed=speed+rspeed
    if tspeed>maxrotorvalue:  #if the total speed is over the allowed max, it will be distributed acordingly
        spd=speed/tspeed*maxrotorvalue
        rspd=rspeed/tspeed*maxrotorvalue
    else:
        spd=speed
        rspd=rspeed

    speed1=spd*math.sin(direction+deg1)+rotate*rspd
    speed2=spd*math.sin(direction+deg2)+rotate*rspd
    speed3=spd*math.sin(direction+deg3)+rotate*rspd
    ser1.write(speed1)#each motor has it's own directional speed and in case of rotation it's rotational speed
    ser2.write(speed2)
    ser3.write(speed3)

    s1 = ser1.read(5)
    readMove(speed1,s1)
    s2 = ser2.read(5)
    readMove(speed2,s2)
    s3 = ser3.read(5)
    readMove(speed3,s3)

    #time.sleep(0.1) #in case the write output is too fast for the rotors

def findMotor(ID): #locates the requested rotor in the COM ports
    ports = ['COM' + str(i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            ser = serial.Serial(port,115200,timeout=1)
            ser.write("?\n")
            text = ser.read(7)
            print port,",response:",text
            if "<id:"+str(ID)+">" in text:
                print "found id: "+str(ID)
                ser.close()
                return port
            ser.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print result,"Requested COM not found."
    COMerror=True #in case a rotor isn't found, this later stops the program
    
def openConnections(COM1,COM2,COM3): #starts communications with the rotors
    print "Opening connections with the requested rotors."
    global ser1,ser2,ser3
    ser1 = serial.Serial(COM1,115200,timeout=1)
    ser2 = serial.Serial(COM2,115200,timeout=1)
    ser3 = serial.Serial(COM3,115200,timeout=1)
    ser1.write("dr0\n") #sets up the rotor directions
    ser2.write("dr0\n")
    ser3.write("dr0\n")
    print "ser1 =",ser1.isOpen(),",ser2 =",ser2.isOpen(),",ser3 =",ser3.isOpen()

def closeConnections(): #ends the session
    print "Closing connections."
    ser1.close()
    ser2.close()
    ser3.close()
    print "ser1 =",ser1.isOpen(),",ser2 =",ser2.isOpen(),",ser3 =",ser3.isOpen()

def setup(): #defines the COM ports and sets up the connections
    COM1=findMotor(servoID1)
    COM2=findMotor(servoID2)
    COM3=findMotor(servoID3)
    if COMerror:
        print "Opening connections aborted."
    else:
        openConnections(COM1,COM2,COM3)

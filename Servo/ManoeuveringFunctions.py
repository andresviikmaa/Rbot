import serial
import math
import time
import re
#servoID1,servoID2,servoID3=0,0,0 #servo ID numbers
deg1,deg2,deg3=4.2,3.1,1 #rotor positions on the machine
deg1,deg2,deg3=4.2,0,2.1 #rotor positions on the machine
maxrotorvalue=19 #max speed the rotor can achieve
COMerror=False #in case a rotor COM is not found

GlobalStop=False
removeString="<s:>\n"

Stallcounter=0

outputless=False
StallReverse=0

Servocounter=1

def readLED():
    try:
        ser2.write("gb\n")

        read=ser2.read(6)
        #return read
        if "1" in read:
            return True
        return False
    except:
        return False
    
def readMove(inputVal,inputString):
    global StallReverse
    inputString=re.search("<stall:(.*)>",inputString)
    if inputString!=None:
        #print inputString.group(1),inputVal
        if inputString.group(1)=="1":
            StallReverse=20
            print "stall"
        if inputString.group(1)=="2":
            GlobalStop=True
            #GlobalStop=False
        if not outputless:
            #print inputString.group(1)
            pass

def move(Values):#speed is movespeed, rspeed is rotational speed, rotate signifies the direction of rotation
    global Stallcounter,StallReverse,Servocounter
    [speed,direction,rspeed]=Values
    #speed=0
    direction=math.radians(direction)
    tspeed=abs(speed)+abs(rspeed)
    if tspeed>maxrotorvalue:  #if the total speed is over the allowed max, it will be distributed acordingly
        spd=speed/float(tspeed)*maxrotorvalue
        rspd=rspeed/float(tspeed)*maxrotorvalue
    else:
        spd=speed
        rspd=rspeed
        
    if GlobalStop:
        speed1=0
        speed2=0
        speed3=0
    else:
        speed1=int(spd*math.sin(direction+deg1)+rspd)
        speed2=int(spd*math.sin(direction+deg2)+rspd)
        speed3=int(spd*math.sin(direction+deg3)+rspd)

    if StallReverse>0:
        speed1=-speed1
        speed2=-speed2
        speed3=-speed3
        StallReverse-=1
    #if not outputless:  
    #    print speed1,speed2,speed3

    
    if Servocounter==1:
        try:
            ser1.write("sd"+str(speed1)+"\n")#each motor has it's own directional speed and in case of rotation it's rotational speed
        except:
            print "ser1 input error"
        #ser1.write("s\n")
    if Servocounter==2:
        try:
            ser2.write("sd"+str(speed2)+"\n")
        except:
            print "ser2 input error"
        #ser2.write("s\n")
    if Servocounter==3:
        try:
            ser3.write("sd"+str(speed3)+"\n")
        except:
            print "ser3 input error"
        #ser3.write("s\n")
        Servocounter=0
    Servocounter+=1

    #print(Stallcounter)
        
##    try:
##        if Stallcounter==4:
##            s1 = ser1.read(10)
##            readMove(speed1,s1)
##        elif Stallcounter==8:
##            s2 = ser2.read(10)
##            readMove(speed2,s2)
##        elif Stallcounter>11:
##            s3 = ser3.read(10)
##            readMove(speed3,s3)
##            Stallcounter=0
##    except:
##        print "servo read error"
##    
##    Stallcounter+=1
    #Stallcounter=4

    #print s1,s2,s3

    #time.sleep(0.1) #in case the write output is too fast for the rotors

def findMotor(ID): #locates the requested rotor in the COM ports
    ports = ['/dev/ttyACM' + str(i) for i in range(256)]
    result = []
    for port in ports:
        try:
            ser = serial.Serial(port,115200,timeout=0.1)
            ser.write("?\n")
            time.sleep(0.1)
            ser.write("gs0\n")
            time.sleep(0.1)
            text = ser.read(10)
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
    ser1.write("dr1\n") #sets up the rotor directions
    ser2.write("dr1\n")
    ser3.write("dr1\n")
    #ser1.write("gs1\n")
    #ser2.write("gs1\n")
    #ser3.write("gs1\n")
    print "ser1 =",ser1.isOpen(),",ser2 =",ser2.isOpen(),",ser3 =",ser3.isOpen()

def closeConnections(): #ends the session
    print "Closing connections."
    ser1.write("gs0\n")
    ser2.write("gs0\n")
    ser3.write("gs0\n")
    time.sleep(0.1)
    ser1.close()
    time.sleep(0.1)
    ser2.close()
    time.sleep(0.1)
    ser3.close()
    print "ser1 =",ser1.isOpen(),",ser2 =",ser2.isOpen(),",ser3 =",ser3.isOpen()

def setup(servoID1,servoID2,servoID3): #defines the COM ports and sets up the connections
    COM1=findMotor(servoID1)
    COM2=findMotor(servoID2)
    COM3=findMotor(servoID3)
    if COMerror:
        print "Opening connections aborted."
    else:
        openConnections(COM1,COM2,COM3)


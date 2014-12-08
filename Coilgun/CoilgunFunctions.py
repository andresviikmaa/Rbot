import serial
import time



def findCoil(ID): #locates the requested rotor in the COM ports
    ports = ['/dev/ttyACM' + str(i) for i in range(256)]
    result = []
    for port in ports:
        try:
            ser = serial.Serial(port,115200,timeout=0.1)
            ser.write("?\n")
            time.sleep(0.1)
            text = ser.read(10)
            print port,",response:",text
            if "<id:"+str(ID)+">" in text or "discharged" in text:
                print "found id: "+str(ID)
                ser.close()
                return port
            ser.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print result,"Requested COM not found."
    #return None
    COMerror=True #in case a coil isn't found, this later stops the program
    

def CoilSetup(ID):
    global coil
    COM=findCoil(ID)
    if COM==None:
        print "Second comm connection attempt."
        COM=findCoil(ID)
    coil = serial.Serial(COM,115200,timeout=1)
    coil.write("c\n")
    coil.write("ac1\n")
    coil.write("fs0\n")

Dribblerstat=False
def Dribbler(onoff):
    global Dribblerstat
    if onoff and not Dribblerstat:
        coil.write("sd16\n")
        Dribblerstat=True
    elif not onoff and Dribblerstat:
        coil.write("sd0\n")
        Dribblerstat=False

def Shoot(time):
    coil.write("k"+str(time)+"\n")
    coil.write("c\n")

def Ping():
    coil.write("p\n")

def closeConnection():
    print "Closing connections."
    Dribbler(False)
    time.sleep(0.5)
    coil.write("ac0\n")
    time.sleep(0.1)
    coil.write("fs1\n")
    time.sleep(0.1)
    coil.close()
    print "coil =",coil.isOpen()

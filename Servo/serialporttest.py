import sys
#import glob
import serial

def findmotor(ID):
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



motor8port=findmotor(7)
print motor8port

a="<s:>"
ser = serial.Serial("COM8",115200,timeout=1)
print ser.name
ser.write("?\n")
s = ser.read(7)
print s
ser.write("sd5\n")
ser.write("s\n")
s = ser.read(5)

for i in a:
    s =s.replace(i,"")
print int(s)
ser.close()

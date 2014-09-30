import serial
import time
ser = serial.Serial("COM8",115200,timeout=1)
print ser.name

ser.write("?\n")
s = ser.read(7)
print s

##ser.write("dr0\n")
##ser.write("sd7\n")
##time.sleep(1)
ser.write("dr0\n")
##ser.write("sd3\n")
b=1
for i in range(1):
    for j in range(50):
        a="sd"+str((50-j)*b)+"\n"
        ser.write(a)
        ser.write("s\n")
        s = ser.read(7)
        print s
        time.sleep(0.1)
    if b==-1:
        b=1
    else:
        b=-1
    

print ser.isOpen()
ser.close()
print ser.isOpen()

import cv2
import numpy as np
import copy
import Tkinter as tk
from threading import Thread,Event
from multiprocessing import Array
from ctypes import c_int32
import Kaamera.lembalemba as lmb
#primaryWrite=True
class CaptureController(tk.Frame):

    NSLIDERS = 6
    atLine=0
    labels="Min Hue", "Min Saturation", "Min Value","Max Hue", "Max Saturation", "Max Value"
    print "Input traced object threshold."
    def __init__(self,parent):
        tk.Frame.__init__(self)
        self.parent = parent

        # create a synchronised array that other threads will read from
        self.ar = Array(c_int32,self.NSLIDERS)

        # create NSLIDERS Scale widgets
        self.sliders = []
        for ii in range(self.NSLIDERS):
            
            # through the command parameter we ensure that the widget updates the sync'd array
            s = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL, label=self.labels[ii],
                         command=lambda pos,ii=ii:self.update_slider(ii,pos))
            s.pack()
            #s.label("hi")
            if ii>2:
                s.set(255)
            self.sliders.append(s)

        # Define a quit button and quit event to help gracefully shut down threads 
        tk.Button(self,text="Quit",command=self.quit).pack()
        self._quit = Event()
        self.capture_thread = None

        tk.Button(self,text="Save",command=self.save).pack()

    # This function is called when each Scale widget is moved
    def update_slider(self,idx,pos):
        self.ar[idx] = c_int32(int(pos))

    # This function launches a thread to do video capture
    def start_capture(self):
        self._quit.clear()
        # Create and launch a thread that will run the video_capture function 
        self.capture_thread = Thread(target=video_capture, args=(self.ar,self._quit))
        self.capture_thread.daemon = True
        self.capture_thread.start()
    def save(self):
        readlines=[]
        #f=open("save.txt","r+")
        if self.atLine==0:
            f=open("save.txt","w")
        elif self.atLine<=5:
            f=open("save.txt","r")
            for line in f:
                readlines.append(line)
            f.close()
            f=open("save.txt","w")
            for line in readlines:
                f.write(line)
        if self.atLine>5:
            print "All values already saved!"
        else:
            print self.ar[:]
            self.atLine+=1
            for i in self.ar[:]:
                f.write(str(i)+" ")
            f.write("\n")
            f.close()
        if self.atLine==1:
            print "Input area threshold."
        elif self.atLine==2:
            print "Input first goal threshold."
        elif self.atLine==3:
            print "Input second goal threshold."
        elif self.atLine==4:
            print "Input black line threshold."
        elif self.atLine==5:
            print "Input white line threshold."
    def emptySave(self):
        while self.atLine<=5:
            readlines=[]
            f=open("save.txt","r")
            for line in f:
                readlines.append(line)
            f.close()
            f=open("save.txt","w")
            for line in readlines:
                f.write(line)
            self.atLine+=1
            f.write("\n")
            f.close()
            print "Empty line saved."
        
    def quit(self):
        self.emptySave()
        self._quit.set()
        try:
            self.capture_thread.join()
        except TypeError:
            pass
        self.parent.destroy()

# This function simply loops over and over, printing the contents of the array to screen
def video_capture(ar,quit):
    cap = cv2.VideoCapture(0)
    lmb.set_cam_settings_from_cli()
    # This while loop would be replaced by the while loop in your original code
    while not quit.is_set():
        #print ar[0]
        ret, frame = cap.read()
    
        lower_values = np.array((ar[0],ar[1],ar[2]))
        upper_values = np.array((ar[3],ar[4],ar[5]))
        
        # smooth it
        frame = cv2.blur(frame,(3,3))

        # convert to hsv and find range of colors
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #thresh = cv2.inRange(hsv,np.array((0, 80, 80)), np.array((20, 255, 255)))
        #thresh2 = thresh.copy()

        #mask
        mask = cv2.inRange(hsv, lower_values, upper_values)
        res = cv2.bitwise_and(frame,frame, mask= mask)

        
            
        #cv2.imshow('frame',frame)
        #cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        
        if cv2.waitKey(1) >= 0:
          break
        
        # the slider values are all readily available through the indexes of ar
        # i.e. w1 = ar[0]
        # w2 = ar[1]
        # etc. 


if __name__ == "__main__":
    root = tk.Tk()
    selectors = CaptureController(root)
    selectors.pack()
    selectors.start_capture()
    root.mainloop()


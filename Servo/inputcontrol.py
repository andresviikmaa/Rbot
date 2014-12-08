import cv2
import numpy as np
import copy
import Tkinter as tk
from threading import Thread,Event
from multiprocessing import Array
from ctypes import c_int32
#primaryWrite=True
class CaptureController(tk.Frame):

    NSLIDERS = 2
    atLine=0
    labels="Move speed", "Turn speed"
    def __init__(self,parent):
        tk.Frame.__init__(self)
        self.parent = parent

        # create a synchronised array that other threads will read from
##        self.ar = Array(c_int32,self.NSLIDERS)
##
##        # create NSLIDERS Scale widgets
##        self.sliders = []
##        for ii in range(self.NSLIDERS):
##            
##            # through the command parameter we ensure that the widget updates the sync'd array
##            s = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL, label=self.labels[ii],
##                         command=lambda pos,ii=ii:self.update_slider(ii,pos))
##
##            s.pack()
##            #s.label("hi")
##            if ii>2:
##                s.set(255)
##            self.sliders.append(s)
##            
        MyButton1=tk.Button(self,text="Move",width=10,command=self.quit)
        MyButton1.pack()
        #MyButton1.grid(row=2, column=0)
        MyButton2=tk.Button(self,text="Move2",width=10,command=self.quit)
        MyButton2.pack()
        #MyButton2.grid(row=2, column=1)
        # Define a quit button and quit event to help gracefully shut down threads 
        MyButton3=tk.Button(self,text="Quit",width=10,command=self.quit)
        MyButton3.pack()
        #MyButton3.grid(row=2, column=2)
        self._quit = Event()
        self.capture_thread = None

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

    def quit(self):
        self._quit.set()
##        try:
##            self.capture_thread.join()
##        except TypeError:
##            pass
        self.parent.destroy()

# This function simply loops over and over, printing the contents of the array to screen
#def video_capture(ar,quit):
    


if __name__ == "__main__":
    root = tk.Tk()
    selectors = CaptureController(root)
    selectors.pack()
    #selectors.start_capture()
    root.mainloop()


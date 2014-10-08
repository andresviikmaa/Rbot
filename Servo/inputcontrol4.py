#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we show how to
use the Scale widget.

author: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
"""

#from ttk import Frame, Label, Scale, Style
import Tkinter
from ctypes import c_int32
from threading import Thread,Event
from multiprocessing import Array
import time
import ManoeuveringFunctions as MF


class Example(Tkinter.Frame):
    #Valueholder=[0,0,0,0]
    NSLIDERS = 3
    Slider_names=["Move speed","Move direction","Turn speed"]
    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        self.ar = Array(c_int32,self.NSLIDERS)
        
        self.parent.title("Scale")
        #self.style = Style()
        #self.style.theme_use("default")        
        
        self.pack(fill=Tkinter.BOTH, expand=1)
        for ii in range(self.NSLIDERS):
            if ii==1:
                maxv=360
            else:
                maxv=255
            if ii<2:
                minv=0
            else:
                minv=-255
            s = Tkinter.Scale(self, from_=minv, to=maxv, orient=Tkinter.HORIZONTAL,label=self.Slider_names[ii],
            command=lambda pos,ii=ii:self.update_slider(ii,pos))
            s.place(x=20, y=10+ii*40)
            s.pack()
        Tkinter.Button(self,text="Quit",command=self.quit).pack()
        self._quit = Event()
        self.capture_thread = None

    def onScale(self, val):
     
        v = int(float(val))
        self.var.set(v)
        print v
    def update_slider(self,idx,pos):
        self.ar[idx] = c_int32(int(pos))
        #print(idx,pos)
        #self.Valueholder[idx]=pos
    def start_capture(self):
        self._quit.clear()
        # Create and launch a thread that will run the video_capture function 
        self.capture_thread = Thread(target=output_loop, args=(self.ar,self._quit))
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
    def quit(self):
        self._quit.set()
        try:
            self.capture_thread.join()
        except TypeError:
            pass
        self.parent.destroy()
         
def output_loop(Valueholder,quit):
    try:
        MF.setup(1,2,3)
    except:
        print "Setup failed"
    while not quit.is_set():
        #print [Valueholder[0],Valueholder[1],Valueholder[2]]
        time.sleep(0.01)
def main():
    root = Tkinter.Tk()
    ex = Example(root)
    ex.pack()
    ex.start_capture()
    #root.geometry("300x150+300+300")
    root.mainloop()  


if __name__ == '__main__':
    main()  

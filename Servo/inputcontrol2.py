#from Tkinter import *
import Tkinter as tk





self = tk.Tk()



tk.Label(self,text='Move speed', relief=tk.RIDGE,width=15).grid(row=0,column=0)
tk.Label(self,text='Turn speed', relief=tk.RIDGE,width=15).grid(row=1,column=0)

S1=tk.Scale(self,from_=0, to=255, orient=tk.HORIZONTAL).grid(row=0,column=1)
S2=tk.Scale(self,from_=0, to=255, orient=tk.HORIZONTAL).grid(row=1,column=1)

tk.Button(self,text="Turn left",width=10,command=self.quit).grid(row=2,column=0)
tk.Button(self,text="Turn right",width=10,command=self.quit).grid(row=2,column=1)
tk.Button(self,text="Move",width=10,command=self.quit).grid(row=3,column=0)
tk.Button(self,text="Quit",width=10,command=self.quit).grid(row=3,column=1)
tk.mainloop()
print S1.get()


import Tkinter

def print_value(val):
    print val

root = Tkinter.Tk()

scale1 = Tkinter.Scale(orient='horizontal', from_=0, to=128, command=print_value)
scale2 = Tkinter.Scale(orient='horizontal', from_=0, to=128, command=print_value)
scale3 = Tkinter.Scale(orient='horizontal', from_=0, to=128, command=print_value)
scale4 = Tkinter.Scale(orient='horizontal', from_=-1, to=1, command=print_value)
scale1.pack()
scale2.pack()
scale3.pack()
scale4.pack()

button=Tkinter.Button(text="Move",width=10,command=print_value(1))
button.pack()

root.mainloop()

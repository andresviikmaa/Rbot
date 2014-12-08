from turtle import *
speed(10)
delay(0)


def move(VALUES):
    [speed,direction,turnspeed]=VALUES
    left(direction)
    forward(speed/100.0)
    right(direction)
    right(turnspeed/10.0)
#move([0,0,0])
##
##for i in range(400):
##    move([9,0,i-200])
##for i in range(400):
##    move([9,i,0])

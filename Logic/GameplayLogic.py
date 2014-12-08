MaxMoveSpeed=255
MaxTurnSpeed=255
Screenx=650.0
Screeny=500.0
MaxSize=20.0
MinSize=10.0
Goalsize=100.0


Goaloldsize=0
GoalCount=0
Goalaverage=[]
import numpy
import math





def Disdance(ydis,size):
    try:
        return 1-(ydis+(size-MinSize)/MaxSize)/2.0
    except:
        return 0
    #return ydis
    

def TurnSpeedCalc(Xset):
    if Xset==0:
        TurnSpeed=0
    else:
        if Xset<0:
            direction=-1
        else:
            direction=1
        try:
            TurnSpeed=(abs(Xset)**2*MaxTurnSpeed*direction)/1.0
        except:
            TurnSpeed=0
    #print MoveSpeed,TurnSpeed
    return int(TurnSpeed/2.0)


def Heading(x):
    try:
        return numpy.arcsin((x-Screenx/2)/(Screenx*1.12))
    except:
        return 0

def ObjectGoto(Values):
    #(650,500)
    [xCor,yCor,size]=Values
    XAmplitude=((xCor/Screenx)*2-1)*-1
    YAmplitude=(Screeny-yCor)/(Screeny)
    #print YAmplitude,XAmplitude
    Mspeed=(((YAmplitude-abs(XAmplitude)+1)/2.0))*MaxMoveSpeed
    Tspeed=TurnSpeedCalc(XAmplitude)
    Direction=math.degrees(Heading(xCor))
    #print(math.degrees(z))
    return [Mspeed,Direction,Tspeed]

def TurnTo(Values,FieldClear):
    global Canshoot,Goalsize,Goaloldsize,GoalCount,Goalaverage
    try:
        [xCor,yCor,Xsize]=Values
        XAmplitude=-((xCor/Screenx)*2-1)
        Tspeed=TurnSpeedCalc(XAmplitude)
        Direction=(Tspeed/abs(Tspeed))*90
        Canshoot=False

        if Xsize>(Goalsize*2): #Test logic when too close to goal
            Direction=180
            Mspeed=(Xsize/(Xsize-Goalsize))*255
        
        if Xsize<Goalsize or FieldClear==False :
            if Goaloldsize>Xsize:
                Direction=10 #<ADD DIRECTION VALUE HERE DEPENDING ON GOAL LOCATION
            else:
                Direction=-10
            #Legroom when assessing the goal old size
            if GoalCount<500:
                Goalaverage.append(Xsize)
                GoalCount+=1
            else:
                Goaloldsize=sum(Goalaverage)/float(len(Goalaverage))
                Goalaverage=[]
                GoalCount=0

            
            Mspeed=(Goalsize/(Goalsize-Xsize))*255
        else:
            if abs(Tspeed)<(Xsize/2)-5:
                Canshoot=True
            Mspeed,Direction=0,0

        return [Mspeed,Direction,Tspeed]
    except:
        return [10,180,10]
        


    

##def visualtest():
##    from turtle import *
##    speed(12)
##    delay(0)
##    back(300)
##    for i in range(650):
##        a=ObjectGoto([i,0,10])[0][0]
##        #b=a
##        b=ObjectGoto([i,250,20])[0]
##        c=ObjectGoto([i,500,30])[0]
##        d=ObjectGoto([i,0,0])[2]
##        left(90)
##        color("blue")
##        forward(a)
##        back(a-b)
##        color("purple")
##        back(b-c)
##        color("red")
##        back(c+d)
##        color("green")
##        forward(d)
##        right(90)
##        forward(1)
##    exitonclick()
##
##def visualtest2():
##    from turtle import *
##    speed(12)
##    delay(0)
##    back(300)
##    for i in range(650):
##        a=TurnTo([0,0,i/6.5])[0]
##        left(90)
##        color("blue")
##        forward(a)
##        back(a)
##        right(90)
##        forward(1)
##    exitonclick()
##    
##def visualtest3():
##    from turtle import *
##    speed(12)
##    delay(0)
##    back(300)
##    for i in range(650):
##        a=ObjectGoto([325,i/650.0*500,0])[0]
##        left(90)
##        color("blue")
##        forward(a)
##        back(a)
##        right(90)
##        forward(1)
##    exitonclick()
#visualtest()

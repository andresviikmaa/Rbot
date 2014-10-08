MaxMoveSpeed=255
MaxTurnSpeed=255
Screenx=650.0
Screeny=500.0
def ObjectGoto(Values):
    #(650,500)

    [xCor,yCor,size]=Values
    XAmplitude=(xCor/Screenx)*2-1
    YAmplitude=(Screeny-yCor-100)/(Screeny-100.0)
    TurnSpeed=XAmplitude**2*MaxTurnSpeed
    MoveSpeed=(((YAmplitude-abs(XAmplitude)+1)/2.0)**2)*MaxMoveSpeed
    #print MoveSpeed,(YAmplitude-abs(XAmplitude)+1),YAmplitude,XAmplitude
    return [MoveSpeed,TurnSpeed]

#for i in range(650):
#    print ObjectGoto([i,500,20])[0],ObjectGoto([i,400,20])[0],ObjectGoto([i,200,20])[0]


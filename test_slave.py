from uartremote import *
from machine import Pin

pins=[5,22,25,2,26,27,32,33,4,21,23,0,12,13,14,15]

ur=UartRemote()

def read_gpio(pin):
    a={}
    for pp in pins:
        p = Pin(pp, Pin.IN, pull=Pin.PULL_DOWN)
        a[pp]=p.value()
    check=True
    print([a[aa] for aa in a])
    for aa in a:
        if aa==pin:
            check&=(a[aa]==1)
        else:
            check&=(a[aa]==0)
    return check


#for p in pins:
#   _=read_gpio(p)
    
ur.add_command(read_gpio,'repr')

ur.loop()


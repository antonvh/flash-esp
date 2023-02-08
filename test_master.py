from uartremote import *
from machine import Pin
from time import sleep_ms
pins = [5,22,25,2,26,27,32,33,4,21,23,0,12,13,14,15]

ur=UartRemote()

def write_gpio(pin,val):
    p = Pin(pin, Pin.OUT)
    p.value(val)
    

def show_pins(check_pins):
    state=[1 if p in check_pins else 0 for p in pins]
    print("[*] -------------------------------------")
    print('[*] '+''.join(["GP%02d "%p for p in pins[:8]]))
    print('[*] '+''.join([" [%1d] "%s for s in state[:8]]))
    print('[*] '+''.join(["GP%02d "%p for p in pins[8:]]))
    print('[*] '+''.join([" [%1d] "%s for s in state[8:]]))
    sleep_ms(500) 

def test():
    check_pins=[]
    for p in pins:
        write_gpio(p,0)
    print("Testing LMS-ESP32")
    print()
    _=input("[?] Press enter to start.")
    for p in pins:
        write_gpio(p,0)
        sleep_ms(20)
        ack,val=ur.call('read_gpio','repr',p)
        check=(val==0)
        write_gpio(p,1)
        sleep_ms(20)
        ack,val=ur.call('read_gpio','repr',p)
        check=check and (val==1)
        if check:
            check_pins.append(p)
        for p in pins:
           write_gpio(p,0)    
    show_pins(check_pins)
        
while (1):
    
    test()
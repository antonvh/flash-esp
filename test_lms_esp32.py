# script to test the connectivity of the different headers on the LMS-ESP32 module


from machine import UART,I2C,Pin
from time import sleep_ms
test_pin=Pin(19,Pin.IN,pull=Pin.PULL_DOWN) # RX pin on LEGO port
pins = [5,22,25,2,26,27,32,33,4,21,23,0,12,13,14,15]
gpio_pins = [Pin(p,Pin.OUT) for p in pins]



def test_lego_port():
    uart=UART(1, baudrate=115200,rx=18,tx=19,timeout=1)
    print("[*] Connect RX and TX pins of LEGO port.")
    _=input("[?] Press ENTER to start LEGO port check.") 
    check_string=b"test string"
    _=uart.write(check_string)
    sleep_ms(100)
    resp=uart.read()
    if resp==check_string:
        print("[*] Lego port UART OK")
    else:
        print("[!] Error! The respons was:",resp)
        print("[!] but should be: ",check_string)
        print("[!] Check the header solder pads")

def check():
    check_pins=[]
    for p in pins:
        check=False
        pin=Pin(p,Pin.OUT)
        sleep_ms(2)
        pin.value(1)
        check=(test_pin.value()==1)
        sleep_ms(2)
        pin.value(0)
        check&=(test_pin.value()==0)
        if check:
            check_pins.append(p)
    return(check_pins)

def test_gpio_port():
    _=check() # Set LEGO RX as input, GPIO pins as as output
    print("[*] Connect the LEGO RX pin with one of the GPIO pins.")
    print("[*] Disconnect I2C devices from Grove's port.")
    print("[*] The corresponsing GPIO pin should be marked as [1].")
    _=input("[?] Press enter to start.")
    while True:
       check_pins=check()
       state=[1 if p in check_pins else 0 for p in pins]
       print("[*] -------------------------------------")
       print('[*] '+''.join(["GP%02d "%p for p in pins[:8]]))
       print('[*] '+''.join([" [%1d] "%s for s in state[:8]]))
       print('[*] '+''.join(["GP%02d "%p for p in pins[8:]]))
       print('[*] '+''.join([" [%1d] "%s for s in state[8:]]))
       sleep_ms(500) 

def test_i2c_port():
    i2c=I2C(1,sda=Pin(5),scl=Pin(4))
    print("[*] Connect an I2C device to the Grove's port")
    _=input("[?] Press enter")
    scan=i2c.scan()
    if len(scan)==0:
        print("[!] No I2C device detected.")
        print("[!] Check Grove's header solder pads")
    else:
        print("[*] I2C device deteced with address"+
              ("es:" if len(scan)>1 else ":"),scan)
        
        

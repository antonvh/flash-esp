# main.py demo uartremote loop
#
from uartremote import *
ur=UartRemote()         # initialize uartremote on default uart and default uart pins
ur.loop()               # start listing for commands received from the remote instance
from esptool import *
import pyboard
import serial.tools.list_ports
import argparse
import os.path
from time import sleep
from sys import platform




parser = argparse.ArgumentParser(description='Flash tpool for LMS-ESP32-V1.')
parser.add_argument('--port',  nargs='?', help='serial port')
parser.add_argument('--baud',  nargs='?', default="460800",help='baud rate')
parser.add_argument('--init-boot', action=argparse.BooleanOptionalAction, default=True,help='Initialize boot.py')
parser.add_argument('firmware',nargs='?',help='Micropython firmware to be written to flash')

args = parser.parse_args()
print(args)

# these are the VID and PID of the CH340 UART USB controller used in the LMS-ESP-V1.0
CH340_VID_PID='1A86:7523' 

if not args.port: # search for serial port
    ports = serial.tools.list_ports.comports()
    print("[*] Searching for serial ports belonging to LMS-ESP32-V1 units...")
    nr=0
    ports_arr=[]
    for port, desc, hwid in sorted(ports):
        if CH340_VID_PID in hwid:
            if nr==0:
                print("\n[*] Found the following port(s):")
            PORT = port
            ports_arr.append(port)
            nr+=1
            print("[+] nr: {} / {}: {} [{}]".format(nr, port, desc, hwid))
            

    if nr==0: # no ports found
        print("\n[!] No CH340 USB devices found! Are you sure an LMS-ESP32 board is connected?")
        exit()
    if nr>1: # more than one port
        portnr=int(input("\n[?] Which port do you want to use? Enter port nr: "))
        PORT = ports_arr[portnr-1]

if args.firmware:
    MPY  = args.firmware
else:
    MPY = "firmware_ESP32_ULAB_LVGL_SPIRAM_20220219-2337.bin"

firmware_exists = os.path.exists(MPY)
if not firmware_exists:
    print(f"\n[!] ERROR: Firmware file {MPY} not found!")
    exit()


# esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
# Erase
print("\n[*] Erasing flash")
main(
    ["--port",PORT,
    "--chip", "esp32",
    "erase_flash"]
    )

# From then on program the firmware starting at address 0x1000:
# esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20190125-v1.10.bin
# Flash
print(f\'n[*] Flashing firmware {MPY}")
main(
    ["--port",PORT,
    "--chip", "esp32",
    "--baud",args.baud,
    "write_flash",
    "-z", "0x1000", MPY]
)


if args.init_boot:
    BOOTPY = "boot.py"
    print('\n[*] waiting for ESp32 to reboot...')
    sleep(2)
    print("[*] Writing boot.py")
    pyb = pyboard.Pyboard(PORT,115200)
    pyb.enter_raw_repl()
    pyb.fs_put(BOOTPY, "boot.py")
    pyb.exit_raw_repl()
    pyb.close()
print("[*] Done")
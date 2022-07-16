from esptool import *
import pyboard
import serial.tools.list_ports
import argparse
import os.path
from time import sleep
from sys import platform

# python 3.9 supports argparse.BooleanOptionalAction
# as work around use action="store_true", etc.

parser = argparse.ArgumentParser(description='Flash tpool for LMS-ESP32-V1.')
parser.add_argument('--port',  nargs='?', help='serial port')
parser.add_argument('--baud',  nargs='?', default="460800",help='baud rate')
parser.add_argument('--upload', action='store_true', default=False,help='Upload Python files, default does not upload')
parser.add_argument('--no_flash', action='store_true', default=False,help='Do not flash firmware, default flashes firmware')

parser.add_argument('firmware',nargs='?',help='Micropython firmware to be written to flash')

args = parser.parse_args()
print(args)

# these are the VID and PID of the CH340 UART USB controller used in the LMS-ESP-V1.0
CH340_VID_PID='1A86:7523' 
CH9102='1A86:55D4'
if not args.port: # search for serial port
    ports = serial.tools.list_ports.comports()
    print("[*] Searching for serial ports belonging to LMS-ESP32-V1 units...")
    nr=0
    ports_arr=[]
    for port, desc, hwid in sorted(ports):
        print(hwid)
        if CH9102 in hwid:
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

if not args.no_flash:
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
    print(f"\n[*] Flashing firmware {MPY}")
    main(
        ["--port",PORT,
        "--chip", "esp32",
        "--baud",args.baud,
        "write_flash",
        "-z", "0x1000", MPY]
    )

    # From then on program the firmware starting at address 0x1000:
    # esptool.py --chip esp32 --port /dev/ttyUSB0 run
    # Run
    print(f"\n[*] Starting {MPY}")
    main(
        ["--port",PORT,
        "--chip", "esp32",
        "run"   ]
    )

if args.upload:
    BOOTPY = "boot.py"
    TESTPY = "test_lms_esp32.py"
    print('\n[*] waiting for ESp32 to reboot...')
    sleep(2)
    print("[*] Writing boot.py and test_lms_esp32.py")
    pyb = pyboard.Pyboard(PORT,115200)
    pyb.enter_raw_repl()
    pyb.fs_put(BOOTPY, "boot.py")
    pyb.fs_put(TESTPY, "test_lms_esp32.py")
    pyb.exit_raw_repl()
      
    pyb.close()
print("[*] Done")

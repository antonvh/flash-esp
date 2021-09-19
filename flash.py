from esptool import *
from time import sleep
import os

PORT = "/dev/cu.usbserial-AH0692NU"
PWD = "python"
MPY = "esp8266-20210902-v1.17.bin"

main(
    ["--port",PORT,
    "erase_flash"]
    )

main(
    ["--port",PORT,
    "--baud","460800",
    "write_flash","--flash_size=detect","0",MPY]
)

print("Press reset on the board within 3s...")
try:
    os.system('say "Press reset on the board within 3 seconds"')
except:
    pass

sleep(5)
s = serial.Serial(PORT, 115200)

# Install webrepl
def read_print_check_exec(exec, check=""):
    sleep(0.5)
    r = s.read(s.in_waiting)
    # print(r)
    if check:
        if not (r[-len(check):] == bytes(check, "UTF-8")):
            print("ERR: ",r[-len(check):], "is not", bytes(check, "UTF-8"))
            return r
        else: print("OK: ", exec)
    s.write(bytes(exec+"\r\n","UTF-8"))

read_print_check_exec("\r\n\r\n")
read_print_check_exec("\r\n\r\n")
read_print_check_exec("import webrepl_setup", check=">>> ")
read_print_check_exec("E", check="(Empty line to quit)\r\n> ")
read_print_check_exec(PWD, check="New password (4-9 chars): ")
read_print_check_exec(PWD, check="Confirm password: ")
read_print_check_exec("y", check="reboot now? (y/n) ")

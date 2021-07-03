from esptool import *
from time import sleep

PORT = "/dev/cu.usbserial-AH0692NU"
PWD="python"

main(
    ["--port",PORT,
    "erase_flash"]
    )

main(
    ["--port",PORT,
    "--baud","460800",
    "write_flash","--flash_size=detect","0","esp8266-20210618-v1.16.bin"]
)

print("Press reset on the board within 3s...")
sleep(3)
s = serial.Serial(PORT, 115200)

# Install webrepl
def read_print_check_exec(exec, check=""):
    sleep(0.5)
    r = s.read(s.in_waiting)
    print(r)
    if check:
        if not (r[-len(check):] == bytes(check, "UTF-8")):
            print(r[-len(check):], "is not", bytes(check, "UTF-8"))
            return r
    s.write(bytes(exec+"\r\n","UTF-8"))

read_print_check_exec("\r\n\r\n")
read_print_check_exec("import webrepl_setup", check=">>> ")
read_print_check_exec("E", check="(Empty line to quit)\r\n> ")
read_print_check_exec(PWD, check="New password (4-9 chars): ")
read_print_check_exec(PWD, check="Confirm password: ")
read_print_check_exec("y", check="reboot now? (y/n) ")

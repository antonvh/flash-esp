# Automated Micropython flashing and WebREPL script
Tools and resources for flashing the newest micropython firmware on an ESP chips over ftdi. 

It also creates a wifi hotspot on the esp, with `micropythoN` as wifi acces code, and `python` as password for the REPL.

## Installation
- git clone [this repo]
- download latest micropython binary
  - [ESP32](https://micropython.org/download/esp32spiram/)
    - update firmware .bin string `MPY` in [flash32.py](flash32.py) to match the download 
  - [ESP8266](https://micropython.org/download/esp8266/)
     - update firmware .bin string `MPY` in [flash.py](flash.py) to match the download 
- Update `PORT` constant in [flash.py](flash.py) to match the usb device for your FTDI cable

## Usage
- Connect the board with FTDI wire.
- `pipenv run python3 flash.py`
- Press reset on the board while pressing the boot button.
- Reset board without boot button pressed when flashing is done. The script asks for it. You have three seconds. 

### Build micropython from source 
micropython latest [source here]https://micropython.org/download/
AMH library latest [source here](https://github.com/antonvh/mpy-robot-tools/tree/master/mpy_robot_tools)

#### ESP32:
ESP32 requires https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/
Micropython Build notes - https://github.com/micropython/micropython/tree/master/ports/esp32

docker run --rm -v -it $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk
```
docker run --rm -v $PWD:/project -w /project espressif/idf make -C mpy-cross
cd ports/esp32
docker run --rm -v $PWD:/project -w /project espressif/idf make submodules
docker run --rm -v $PWD:/project -w /project espressif/idf make BOARD=GENERIC_SPIRAM
```
esptool.py --baud 115200 --port /dev/cu.usbserial-1410 read_flash 0x0 0x400000 fw-backup-AMH.bin
esptool.py --port /dev/tty.usbserial-1420 --baud 460800 write_flash --flash_size=detect -fm dio 0 AMH-fw-backup.bin

#### ESP8266:
ESP8266 requires https://github.com/pfalcon/esp-open-sdk 
Micropython Build notes https://github.com/micropython/micropython/tree/master/ports/esp8266 

example build commands using docker:
micropython source to a build directory and enter working directory
cp PORTSETTINGS to build directory ports/
cp AMH-MPY-libraries to build directory ports/esp8266/modules/

```
docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make -C mpy-cross
cd ports/esp8266
docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make submodules
docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make
```
however in docker you will not be able to use your attached USB
esptool.py --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect -fm dio 0 firmware.bin

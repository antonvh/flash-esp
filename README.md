# Automated Micropython flashing and WebREPL script
This flashes the newest micropython firmware on an ESP8266 chip over ftdi. It also creates a wifi hotspot on the esp, with `micropythoN` as wifi acces code, and `python` as password for the REPL.
## ESP32
The firmware `firmware_ESP32_ULAB_LVGL_SPIRAM_20220716-1006.bin` is the latest v1.19.1, altough the version promt shows still v1.18. When you do

```
>>> import os
>>> os.uname()
(sysname='esp32', nodename='esp32', release='1.19.1', version='v1.18-1246-g6ebf96a90-dirty on 2022-07-16', machine='ESP32 module (lvgl,ulab,spiram) with ESP32')
```
You will see that the version is 1.19.1.

Flash this version using:
```
python flash32.py 
```

It should automatically find the right com port and uses the latest version of the firmware.

## Installation
- pip install pyserial
- git clone [this repo]
- download latest micropython from https://micropython.org/download/esp8266/ in the repo clone folder
- update firmware .bin string `MPY` in [flash.py](flash.py) to match the download 
- Update `PORT` constant in [flash.py](flash.py) to match the usb device for your FTDI cable

## Usage
- Connect the board with FTDI wire.
- `pipenv run python3 flash.py`
- Press reset on the board while pressing the boot button.
- Reset board without boot button pressed when flashing is done. The script asks for it. You have three seconds. 
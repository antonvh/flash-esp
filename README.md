# Automated Micropython flashing and WebREPL script
This flashes the newest micropython firmware on an ESP8266 chip over ftdi. It also creates a wifi hotspot on the esp, with `micropythoN` as wifi acces code, and `python` as password for the REPL.

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
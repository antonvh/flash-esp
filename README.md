# Automated Micropython flashing and WebREPL script

## Installation
- git clone [this repo]
- download latest micropython from https://micropython.org/download/esp8266/ in the repo clone folder
- update firmware bin name string in flash.py
- update port name string in flash.py

## Usage
- Connect the board with FTDI wire
- `pipenv shell`
- `python3 flash.py`
- Reset board with boot button pressed
- Reset board without boot button pressed when flashing is done. The script asks for it. You have three seconds.
import network
import webrepl

ap = network.WLAN(network.AP_IF)
WPA2PSK = 3
WPAPSK = 2
ap.config(essid="ESP-AP", password="micropythoN", authmode=WPA2PSK)
ap.config(max_clients=2)
ap.active(True)

webrepl.start(password="")
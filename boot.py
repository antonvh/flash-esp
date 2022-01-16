import network
import webrepl

ap = network.WLAN(network.AP_IF)
ap.config(essid="ESP-AP", password="micropythoN")
ap.config(max_clients=2)
ap.active(True)

webrepl.start(password="")
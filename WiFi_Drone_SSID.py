from time import sleep
from djitellopy import Tello


tello = Tello()

# Connect to Tello.
tello.connect()
# Enable mission pads.

tello.set_wifi_credentials(ssid= "Smil", password= "")

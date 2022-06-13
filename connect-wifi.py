from djitellopy import Tello
from time import sleep

tello = Tello()

tello.connect()
tello.connect_to_wifi('RoboticsClub', 'RoboticsClub123@')

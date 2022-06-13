from ast import If
from sre_parse import State
from time import sleep
from djitellopy import Tello

tello = Tello()



tello.connect()

tello.enable_mission_pads()
tello.takeoff()



while 1:
	tello.get_mission_pad_id()
	print(tello.get_mission_pad_id())


	tello.go_xyz_speed_mid(40, 0, 80, 20, 1)

	if tello.get_mission_pad_id() == 6:
		print(tello.get_mission_pad_id())
		break


# tello.go_xyz_speed_mid(130, 0, 20, 40, 1)

# tello.go_xyz_speed_mid(0, 0, 0, 40, 2)

# tello.flip('b')
# tello.flip('l')
# tello.flip('r')

tello.go_xyz_speed_mid(0, 0, 30, 10, 6)

tello.land()
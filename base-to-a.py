from time import sleep
from djitellopy import Tello

class Point:
	# The point's coordinates in 3D space.
	x = 0
	y = 0
	z = 0
	def __init__(self, x, y, z) -> None:
		self.x = x
		self.y = y
		self.z = z


tello = Tello()

# Connect to Tello.
tello.connect()
# Enable mission pads.
tello.enable_mission_pads()
# Takeoff.
tello.takeoff()

A = Point(40, 40, 100)

while True:
	# If mission pad 1 is recognized, fly to A and back.
	if(tello.get_mission_pad_id() == 1):
		tello.go_xyz_speed_mid(A.x, A.y, A.z, 30, 1)
		tello.go_xyz_speed(-A.x, -A.y, 0, 30)
		tello.go_xyz_speed_mid(0, 0 , 100, 30, 1)
		tello.land()

	


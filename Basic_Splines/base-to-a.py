from time import sleep
from djitellopy import Tello
from dataclasses import dataclass

@dataclass      # Point(x,y,z) in 3D space
class Point:
    x: float
    y: float
    z: float

tello = Tello()
tello.connect()
tello.enable_mission_pads()
tello.takeoff()

A = Point(40, 40, 30)

# Move to point A with mission pad 1 as reference.
tello.go_xyz_speed_mid(A.x, A.y, A.z, 50, 1)

# Return to mission pad 1 with A as reference.
tello.go_xyz_speed(-A.x, -A.y, 0, 30)

# Mission pad 1 identification loop. When the drone recognizes mission pad 1
# (20 tries total) then it moves over it and then proceeds to land.
if(tello.get_mission_pad_id() == 1):
	i = 0
	while i < 20:
		tello.go_xyz_speed_mid(0, 0 , 30, 30, 1)
		tello.land()
		i += 1
	


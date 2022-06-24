# Code for 8 - trajectory with landmark references

from djitellopy import Tello
from dataclasses import dataclass
from time import sleep

@dataclass      # Point(x,y,z) dataclass
class Point:
    x: float
    y: float
    z: float

tello = Tello()

tello.connect()

tello.enable_mission_pads()
tello.set_mission_pad_detection_direction(0)

tello.takeoff() 

## Define points
#  Points of Trajectory 1
A1 = Point(0, 0, 30)
B1 = Point(50, 50, 100)
C1 = Point(100, 0, 100)

#  Points of Trajectory 2
A2 = Point(0, 0, 100)
B2 = Point(60, -60, 100)
C2 = Point(120, 0, 100)

#  Points of Trajectory 3
A3 = Point(0, 0, 100)
B3 = Point(-60, 60, 100)
C3 = Point(-120, 0, 100)

#  Points of Trajectory 4
A4 = Point(0, 0, 0)
B4 = Point(-60, -60, 100)
C4 = Point(-120, 0, 100)

## Trajectories

i = 0
while (i <= 5):
    print(tello.get_mission_pad_id())
    i += 1

tello.go_xyz_speed_mid(A1.x, A1.y, A1.z, 40, 1)   # Initialize height


tello.curve_xyz_speed_mid(B1.x, B1.y, B1.z, C1.x, C1.y, C1.z, 40, 1)    # Trajectory 1
sleep(5)
i = 0
while (1):
    print(tello.get_mission_pad_id())
    tello.go_xyz_speed_mid(0, 0, 100, 40, 2)
    i += 1


# tello.curve_xyz_speed_mid(B2.x, B2.y, B2.z, C2.x, C2.y, C2.z, 40, 2)    # Trajectory 2
# tello.curve_xyz_speed_mid(B3.x, B3.y, B3.z, C3.x, C3.y, C3.z, 40, 3)    # Trajectory 3
# tello.curve_xyz_speed_mid(B4.x, B4.y, B4.z, C4.x, C4.y, C4.z, 40, 2)    # Trajectory 4

tello.land()
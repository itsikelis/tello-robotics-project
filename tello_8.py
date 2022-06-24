# Code for 8 - trajectory without landmark references

from djitellopy import Tello
from dataclasses import dataclass

@dataclass      # Point(x,y,z) dataclass
class Point:
    x: float
    y: float
    z: float

tello = Tello()

tello.connect()

tello.enable_mission_pads()

tello.takeoff() 

## Define points
#  Points of Trajectory 1
A1 = Point(0, 0, 30)
B1 = Point(50, 50, 0)
C1 = Point(100, 0, 0)

#  Points of Trajectory 2
A2 = Point(0, 0, 0)
B2 = Point(50, -50, 0)
C2 = Point(100, 0, 0)

#  Points of Trajectory 3
A3 = Point(0, 0, 0)
B3 = Point(-50, 50, 0)
C3 = Point(-100, 0, 0)

#  Points of Trajectory 4
A4 = Point(0, 0, 0)
B4 = Point(-50, -50, 0)
C4 = Point(-100, 0, 0)

## Trajectories
tello.go_xyz_speed(A1.x, A1.y, A1.z, 40)   # Initialize height
tello.curve_xyz_speed(B1.x, B1.y, B1.z, C1.x, C1.y, C1.z, 40)    # Trajectory 1
tello.curve_xyz_speed(B2.x, B2.y, B2.z, C2.x, C2.y, C2.z, 40)    # Trajectory 2
tello.curve_xyz_speed(B3.x, B3.y, B3.z, C3.x, C3.y, C3.z, 40)    # Trajectory 3
tello.curve_xyz_speed(B4.x, B4.y, B4.z, C4.x, C4.y, C4.z, 40)    # Trajectory 4

tello.land()
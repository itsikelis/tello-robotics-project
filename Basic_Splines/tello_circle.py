from djitellopy import Tello
from dataclasses import dataclass

@dataclass      # Point(x,y,z) in 3D space
class Point:
    x: float
    y: float
    z: float

tello = Tello()
tello.connect()
tello.takeoff()

## Define points
#  Points of Semi-Circle 1
A1 = Point(0, 0, 20)
B1 = Point(50, 50, 0)
C1 = Point(100, 0, 0)

#  Points of Semi-Circle 2
A2 = Point(0, 0, 0)
B2 = Point(-50, -50, 0)
C2 = Point(-100, 0, 0)

tello.go_xyz_speed(A1.x, A1.y, A1.z, 40)   # Initialize height
tello.curve_xyz_speed(B1.x, B1.y, B1.z, C1.x, C1.y, C1.z, 40)    # Semi-Circle 1
tello.curve_xyz_speed(B2.x, B2.y, B2.z, C2.x, C2.y, C2.z, 40)    # Semi-Circle 2

tello.land()
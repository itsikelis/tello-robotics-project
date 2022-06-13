from time import sleep
from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()

for i in range(2):
	tello.move_forward(50)
	tello.rotate_counter_clockwise(90)
	tello.move_forward(50)
	tello.rotate_counter_clockwise(90)
	tello.move_forward(50)
	tello.rotate_counter_clockwise(90)
	tello.move_forward(50)

tello.land()


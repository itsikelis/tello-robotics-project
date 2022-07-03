from time import sleep
from djitellopy import Tello

tello = Tello()
tello.connect()
tello.takeoff()

# Square path execution loop.
n = 1	# Number of square paths to be executed.
for i in range(n):
	# The drone moves forward and then rotates 90 degrees clockwise.
	# By repeating this action 4 times, a square path is formed.
	for j in range(4):
		tello.move_forward(50)
		tello.rotate_counter_clockwise(90)

tello.land()
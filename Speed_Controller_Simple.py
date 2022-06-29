from time import sleep
from tracemalloc import start
from turtle import done
from djitellopy import Tello
import time

tello = Tello()

tello.connect()
tello.takeoff()

# for i in range(2):
# 	tello.move_forward(50)
# 	tello.rotate_counter_clockwise(90)
# 	tello.move_forward(50)
# 	tello.rotate_counter_clockwise(90)
# 	tello.move_forward(50)
# 	tello.rotate_counter_clockwise(90)
# 	tello.move_forward(50)

done = False
tick = 0
print("start")
tim = time.perf_counter()
breaking = False
while not done:


    tick+=1
    print("Tick: ", tick)

    # tello.move_forward(10)
    # dictio = tello.get_current_state()
    # print(dictio)
    # tello.go_xyz_speed(1, 0, 0, 10)
    print(time.perf_counter() - tim )
    while (time.perf_counter() - tim < 1):

        tello.send_rc_control(0, 30, 0, 0)
        breaking = True

    if breaking:
        tim2 = time.perf_counter()
        while (time.perf_counter() - tim2 < 0.05):
            tello.send_rc_control(0, 0, 0, 0)
            breaking = False

    if tick >=60:
        done = True



tello.land()


from djitellopy import TelloSwarm
import time


def Search(i, tello, boom):
    while boom[i]:
        tello.send_rc_control(0, 10, 0, 0)
        print(i, tello.get_mission_pad_id())
        if tello.get_mission_pad_id() != -1:
            tello.send_rc_control(0, 0, 0, 0)
            boom[i] = False
        time.sleep(1)

swarm = TelloSwarm.fromIps([
    "192.168.43.127", "192.168.43.248"
])

swarm.connect()
for tello in swarm:
    tello.enable_mission_pads()

swarm.takeoff()


swarm.parallel(lambda i, tello: tello.go_xyz_speed(0, 0, -20, 40))

while True:

    tim = time.perf_counter()
    while time.perf_counter() - tim < 5:
        swarm.parallel(lambda i, tello: tello.go_xyz_speed_mid(
            0, 0, 30, 30, tello.get_mission_pad_id()))
        swarm.sequential(lambda i, tello: print(tello.get_mission_pad_id()))
    swarm.parallel(lambda i, tello: tello.move_forward(35))
    swarm.parallel(lambda i, tello: tello.send_rc_control(0, 10, 0, 0))
    swarm.parallel(lambda i, tello: tello.send_rc_control(0, 0, 0, 0))
    swarm.parallel(lambda i, tello: tello.move_up(60))
    tim = time.perf_counter()
    while time.perf_counter() - tim < 5:
        swarm.parallel(lambda i, tello: tello.send_rc_control(0, 0, 0, 0))
        # swarm.sequential(lambda i, tello: print(tello.get_mission_pad_id()))

    boom = [True, True]
    while True:
        swarm.parallel(lambda i, tello: Search(i, tello, boom))
        swarm.sync
        break

    tim = time.perf_counter()
    while time.perf_counter() - tim < 5:
        swarm.parallel(lambda i, tello: tello.go_xyz_speed_mid(
            0, 0, 30, 10, tello.get_mission_pad_id()))

        swarm.sequential(lambda i, tello: print(tello.get_mission_pad_id()))

    tim = time.perf_counter()
    while time.perf_counter() - tim < 0.5:
        swarm.parallel(lambda i, tello: tello.send_rc_control(0, 0, -5, 0))

    break




    # while boom[1] or boom[2] :
    #     swarm.parallel(lambda i, tello: tello.go_xyz_speed_mid(0, 0, 40, 10, tello.get_mission_pad_id()))
    #     swarm.sequential(lambda i, tello: print(i, tello.get_mission_pad_id()))


# tello.go_xyz_speed_mid(A.x, A.y, A.z, 50, 1)
# run in parallel on all tellos
# swarm.move_down(30)
# swarm.move_down()
# swarm.flip('f')
# swarm.flip('b')

# run by one tello after the other
# swarm.sequential(lambda i, tello: tello.move_forward(i * 20 + 20))

# making each tello do something unique in parallel
# swarm.move_left( 50 + 20)
# swarm.move_forward( 50 + 20)
# swarm.move_right( 50 + 20)
# swarm.move_back( 50 + 20)

swarm.land()
swarm.end()

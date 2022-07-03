from djitellopy import TelloSwarm
import time


# Search Function for parallel use of spatial search
# Contains Controller for Pad Searching, no Reference
def Search(i, tello, boom):
    while boom[i]:
        tello.send_rc_control(0, 10, 0, 0)
        print(i, tello.get_mission_pad_id())
        if tello.get_mission_pad_id() != -1:
            tello.send_rc_control(0, 0, 0, 0)
            boom[i] = False
        time.sleep(1)


# Set the swarm mode and get connection MAC-Addresses
swarm = TelloSwarm.fromIps([
    "192.168.43.127", "192.168.43.248"
])


# Connect to the Swarm
swarm.connect()

# Enable mission pads on both Tellos 
for tello in swarm:
    tello.enable_mission_pads()

# Take of for entire swarm
swarm.takeoff()

# Go to certain high for initialization for entire swarm
swarm.parallel(lambda i, tello: tello.go_xyz_speed(0, 0, -20, 40))

# Loop Function, Space for Inheriting Controllers
while True:

    # Get time
    tim = time.perf_counter()

    # For 5 seconds remain above the pad that exists underneath
    while time.perf_counter() - tim < 5:
        swarm.parallel(lambda i, tello: tello.go_xyz_speed_mid(
            0, 0, 30, 30, tello.get_mission_pad_id()))
        swarm.sequential(lambda i, tello: print(tello.get_mission_pad_id()))

    #Move forward and try to catch wait    
    swarm.parallel(lambda i, tello: tello.move_forward(35))
    swarm.parallel(lambda i, tello: tello.send_rc_control(0, 10, 0, 0))

    #Pick up and remain stationery
    swarm.parallel(lambda i, tello: tello.send_rc_control(0, 0, 0, 0))

    #Set the payload at certain hight
    swarm.parallel(lambda i, tello: tello.move_up(60))

    tim = time.perf_counter()
    #For 5 seconds remain in the previous Hight
    while time.perf_counter() - tim < 5:
        swarm.parallel(lambda i, tello: tello.send_rc_control(0, 0, 0, 0))
        # swarm.sequential(lambda i, tello: print(tello.get_mission_pad_id()))


    #Call the Search function to find the next pads somewhere in front
    boom = [True, True]
    while True:
        swarm.parallel(lambda i, tello: Search(i, tello, boom))
        swarm.sync
        break

    
    tim = time.perf_counter()
    #For 5 seconds remain above the new pads that were found by Search
    while time.perf_counter() - tim < 5:
        swarm.parallel(lambda i, tello: tello.go_xyz_speed_mid(
            0, 0, 30, 10, tello.get_mission_pad_id()))

        swarm.sequential(lambda i, tello: print(tello.get_mission_pad_id()))


    tim = time.perf_counter()

    #For 5 seconds lower the height to set the payload down
    while time.perf_counter() - tim < 0.5:
        swarm.parallel(lambda i, tello: tello.send_rc_control(0, 0, -5, 0))

    break



    # Check for continuity 
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


# Land after setting the payload on target
swarm.land()
swarm.end()

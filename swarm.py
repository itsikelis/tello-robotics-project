from djitellopy import TelloSwarm

swarm = TelloSwarm.fromIps([
    "192.168.1.21"
    , "192.168.1.22"
])

swarm.connect()
swarm.takeoff()

# run in parallel on all tellos
swarm.move_up(70)
swarm.flip('f')
swarm.flip('b')

# run by one tello after the other
# swarm.sequential(lambda i, tello: tello.move_forward(i * 20 + 20))

# making each tello do something unique in parallel
swarm.parallel(lambda i, tello: tello.move_left(i * 100 + 20))
swarm.parallel(lambda i, tello: tello.move_forward(i * 100 + 20))
swarm.parallel(lambda i, tello: tello.move_right(i * 100 + 20))
swarm.parallel(lambda i, tello: tello.move_back(i * 100 + 20))

swarm.land()
swarm.end()

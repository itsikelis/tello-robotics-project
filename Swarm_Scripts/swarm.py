from djitellopy import TelloSwarm

swarm = TelloSwarm.fromIps([
    "192.168.0.123"
    , "192.168.0.124"
])

swarm.connect()
swarm.takeoff()

# run in parallel on all tellos
swarm.move_down(30)
swarm.flip('f')
swarm.flip('b')

# run by one tello after the other
# swarm.sequential(lambda i, tello: tello.move_forward(i * 20 + 20))

# making each tello do something unique in parallel
swarm.move_left( 50 + 20)
swarm.move_forward( 50 + 20)
swarm.move_right( 50 + 20)
swarm.move_back( 50 + 20)

swarm.land()
swarm.end()

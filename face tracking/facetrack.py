from functions import *
import cv2
 
w, h = 640, 480             # Frame width, height

pidYaw = [0.2, 0, 0.6]      # Yaw PID controller gains kP, kI, kD
pidFB =  [0.2, 0 ,0.6]      # Forward/Backward position PID controller gains

pErrorYaw = 0               # Initialize yaw error
pErrorFB = 0                # Initialize forward/backward position error

startCounter = 0            # 0: flight, 1: no flight
 
tello = initializeTello()
 
while True:     # Control Loop
 
    # Flight
    if startCounter == 0:
        tello.takeoff()
        tello.go_xyz_speed(0, 0, 100, 40)
        startCounter = 1
 
    # Step 1
    img = telloGetFrame(tello, w, h)
    
    # Step 2
    img, info = findFace(img)
    
    # Step 3
    pErrorYaw = trackFace(tello, info, w, pidYaw, pErrorYaw, pidFB, pErrorFB)
    #print(info[0][0])
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.land()
        break

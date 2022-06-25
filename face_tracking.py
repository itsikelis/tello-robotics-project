import numpy as np
import cv2
from djitellopy import Tello

tello = Tello()
tello.connect()
print(tello.get_battery())

tello.streamon()
tello.takeoff()
tello.go_xyz_speed(0, 0, 100, 40)

w, h = 360, 240             # image width and height
fbRange = [6200, 6800]      # minimum and maximum detected face areas (forward and backward movement)
PID = [0.4, 0.4, 0]         # PID contoller gains kP, kI, kD
prevError = 0

def faceRecognition(img):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # turn image to grayscale

    scaleFactor = 1.2
    minNeighbors = 8
    faces = faceCascade.detectMultiScale(imgGray, scaleFactor, minNeighbors)

    face_list_centered = []
    face_list_area = []

    for (x,y,w,h) in faces:
        # Rectangular area & center circle
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
        cx = x + w // 2     # circle center coordinates need to be integers, not floats
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx,cy), 5, (0,255,0), cv2.FILLED)
        face_list_centered.append([cx, cy])
        face_list_area.append(area)

    if len(face_list_area) != 0:
        i = face_list_area.index(max(face_list_area))   # index of max value
        return img, [face_list_centered[i], face_list_area[i]]
    else:
        return img, [[0, 0], 0]

def faceTracking(tello, info, w, PID, prevError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2      # deviation between center value and measurement (for angle control)
    speed = PID[0]*error + PID[1]*(error - prevError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]: # area within limits -> no movement
        fb = 0
    elif area > fbRange[2]:                     # area too large -> move backwards
        fb = -20
    elif area < fbRange[0] and area != 0:       # area too small -> move forward
        fb = 20
    if x == 0:      # loss of vision -> stop moving
        speed = 0
        error = 0

    tello.send_rc_control(0, fb, 0, speed)
    return error

while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = faceRecognition(img)

    # PID Control
    prevError = faceTracking(tello, info, w, PID, prevError)
    #qqprint("Center:", "x=", info[0][0], "y=", info[0][1]," Area:", info[1])   # Print observed area and center coordinates
    faceRecognition(img)
    cv2.imshow("Laptop Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):   # land when press Q
        tello.land()
        break
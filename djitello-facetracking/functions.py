from djitellopy import Tello
import cv2
import numpy as np
 
 
def initializeTello():
    tello = Tello()
    tello.connect()
    tello.for_back_velocity = 0
    tello.left_right_velocity = 0
    tello.up_down_velocity = 0
    tello.yaw_velocity = 0
    tello.speedYaw = 0
    print(tello.get_battery())
    tello.streamon()
    return tello
 
def telloGetFrame(tello, w, h):
    myFrame = tello.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img
 
def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    scaleFactor = 1.2
    minNeighbors = 8
    faces = faceCascade.detectMultiScale(imgGray, scaleFactor, minNeighbors)
 
    myFaceListC = []        # Initialize face center coordinate list
    myFaceListArea = []     # Initialize face rectangle area list
 
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)    # Rectangle around face
        cx = x + w // 2         # Center coordinates must be integers, hence integer division //
        cy = y + h // 2
        area = w * h            # Frame area
        cv2.circle(img, (cx, cy), 5, (0,255,0), cv2.FILLED)     # Circle at center of rectangle
        myFaceListArea.append(area)
        myFaceListC.append([cx, cy])
 
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]
 
def trackFace(tello, info, w, pidYaw, pErrorYaw, pidFB, pErrorFB):
    x_m, y_m = info[0]          # measured x, y coordinates
    area = info[1]
    area_range = [6000, 7000]   # minimum and maximum detected face areas (forward and backward movement)
 
    # Yaw angle PID
    errorYaw = x_m - w // 2         # deviation between center value and measurement
    speedYaw = pidYaw[0] * errorYaw + pidYaw[2] * (errorYaw - pErrorYaw)    # PD Conroller Implementation
    speedYaw = int(np.clip(speedYaw, -80, 80))                              # yaw speed saturation control

    if x_m != 0:                            # yaw != 0 -> spin cw/ccw
        tello.yaw_velocity = speedYaw
    else:                                   # yaw = 0 -> no spin
        tello.for_back_velocity = 0
        tello.left_right_velocity = 0
        tello.up_down_velocity = 0
        tello.yaw_velocity = 0
        errorYaw = 0                   # yaw error refresh
    
    '''# Forward - Backward position PID
    errorFB = (area_range[0] + area_range[1]) // 2 - area            # deviation between measured frame area and mean reference freame area
    speedFB = pidFB[0] * errorFB + pidFB[2] * (errorFB - pErrorFB)   # PD Controller Implementation
    speedFB = int(np.clip(speedFB, -30, 30))                         # forward/backwards speed saturation control

    if area < area_range[0] or area > area_range[1]:    # area outside limits -> move forward/backwards
        tello.for_back_velocity = speedFB
    else:                                                # area within limits -> no movement
        tello.for_back_velocity = 0
        tello.left_right_velocity = 0
        tello.up_down_velocity = 0
        tello.yaw_velocity = 0
        errorFB = 0                   # forward/backward position error refresh'''

    if tello.send_rc_control:
        tello.send_rc_control(tello.left_right_velocity,
                              tello.for_back_velocity,
                              tello.up_down_velocity,
                              tello.yaw_velocity)
    return errorYaw
    #return errorFB

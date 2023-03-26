import cv2
import mediapipe as mp      #an ML lib can be used for hand detection, face detection etc. without youself building an model and training it
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vRange = volume.GetVolumeRange()              #getting the volume range as it varies in windows 
minv,maxv = vRange[0],vRange[1]               #assing minimun and maximum volume




mp_hands = mp.solutions.hands
draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()


capture = cv2.VideoCapture(0)              #capturing the screen frame by frame
while True:
    value,image = capture.read()              #reading the image 
    rgbimage = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)         #converting the BGR color scheme to RGB, because to process the image with mediapipe lib it needs image in RGB
    processed_image = hands.process(rgbimage)
    print(processed_image.multi_hand_landmarks)    #draw points on the hand(mainly joints) total of 28 points on the hand 
    if(processed_image.multi_hand_landmarks):
        for handLandmarks in processed_image.multi_hand_landmarks:
            for finger_id,landmark_co in enumerate(handLandmarks.landmark):
                height,width,channel = image.shape             
                cx,cy = int(landmark_co.x*width), int(landmark_co.y*height)       
                if finger_id == 4:         #finger id for thumb is 4
                    cv2.circle(image,(cx,cy),30,(255,0,255),cv2.FILLED)     #drawing circle on thumb
                    tpx,tpy = cx,cy
                if finger_id == 8:         #finger if for index finger is 8(availabe in doc of mediapipe)
                    cv2.circle(image,(cx,cy),30,(255,0,255),cv2.FILLED)     #drawing circle on index finger 
                    ipx,ipy = cx,cy 
                    cv2.line(image,(tpx,tpy),(ipx,ipy),(0,255,0),9)        #drawing line from thumb to index finger
                    distance = math.sqrt((tpx-ipx)**2 + (tpy-ipy)**2)      #getting distance between thumb and index finger(square and sq rooting so that value does not comes as negative)
                    print(distance)
                    v = np.interp(distance,[25,250],[minv,maxv])      #interpreting distance bewteen thumb and index finger with the max and min volume of the system
                    volume.SetMasterVolumeLevel(v, None)              #controlling volume with gesture

            draw.draw_landmarks(image, handLandmarks,mp_hands.HAND_CONNECTIONS)
    cv2.imshow('Image Capture', image)
    if cv2.waitKey(1) & 0xFF==27:     #close the capture when esc is pressed
        break

capture.release()           #stop the image capture 
cv2.destroyAllWindows()     #destroy all captured iamge so that it does not consume system resources
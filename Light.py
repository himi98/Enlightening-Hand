import cv2
import numpy as np
import pyautogui
from matplotlib import pyplot as plt
import time
import requests
cap = cv2.VideoCapture(0)
ct=0
ct1=0
time.sleep(5)
while(1):

    _, frame = cap.read()
    frame=cv2.flip(frame,1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0,48,80])
    upper_blue = np.array([20,255,255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    blur = cv2.GaussianBlur(mask,(15,15),0)
    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('thresh',thresh)
    _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if not contours:
        continue
    cnt = contours[0]
    if(len(contours))>=0:
        c=max(contours, key=cv2.contourArea)
        (x,y),radius=cv2.minEnclosingCircle(c)
        M=cv2.moments(c)
    else:
        print("Sorry no contour found")
    cnt=c
    if cv2.contourArea(cnt)<=1000:
        continue
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count=0;
    try:
        defects.shape
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            cv2.line(frame,start,end,[0,255,0],2)
            cv2.circle(frame,far,5,[0,0,255],-1)
            count=count+1
        #print(str(cv2.contourArea(cnt,True)))
        if cv2.arcLength(cnt,True)>2000:
            while ct==0:
                print("ON")
                f = requests.get("http://192.168.43.147/LEDOn")
                ct=ct+1
                ct1=0
        elif cv2.arcLength(cnt,True)>500 and cv2.arcLength(cnt,True)<=1500:
            while ct1==0:
                print("OFF")
                f = requests.get("http://192.168.43.147/LEDOff")
                ct1=ct1+1
                ct=0

    except AttributeError:
        print("shape not found")    
    cv2.imshow('final',frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    

cv2.destroyAllWindows()

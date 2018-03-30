import cv2
import numpy as np
import pyautogui
from matplotlib import pyplot as plt
import time

cap = cv2.VideoCapture(0)
ct=0
ct1=0
time.sleep(5)
while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([0,48,80])
    upper_blue = np.array([20,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    #res = cv2.GaussianBlur(res,(10,10),0)
    blur = cv2.GaussianBlur(mask,(15,15),0)

    #Apply threshold
    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
   
    cv2.imshow('frame',mask)
    #cv2.imshow('ret',ret)
    cv2.imshow('thresh',thresh)
    #img = thresh
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
    #epsilon = 0.01*cv2.arcLength(cnt,True)
    #approx = cv2.approxPolyDP(cnt,epsilon,True)
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
                pyautogui.press('space')
                ct=1
                ct1=0
        if cv2.arcLength(cnt,True)>500 and cv2.arcLength(cnt,True)<=1500:
            while ct1==0:
                print("OFF")
                pyautogui.press('space')
                ct1=1
                ct=0

        #if arc
    except AttributeError:
        print("shape not found")    
    cv2.imshow('final',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    cv2.imshow('mask', mask)
   # cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    

cv2.destroyAllWindows()

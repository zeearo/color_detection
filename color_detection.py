#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')  ##%matplotlib.inline
import time


# In[2]:


def pick_image():
    img_name= input('Write the image file name here:')
    image= cv2.imread(img_name)
    image= cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image


# In[3]:


index=['COLOR','COLOR_NAME','HEXA','R','G','B']
csv=pd.read_csv('colors.csv',names=index,header=None)


# In[4]:


def color_finder(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        global b,g,r,clicked 
        clicked= True
        b,g,r= img[y,x]
        b=int(b)
        g=int(g)
        r=int(r)


# In[5]:


def find_color_name(R,G,B):
    minimum= 9999
    for i in range(len(csv)):
        data= abs(R-int(csv.loc[i,"R"]))+abs(G-int(csv.loc[i,"G"]))+ abs(B-int(csv.loc[i,"B"]))
        if(data<=minimum):
            minimum=data
            colorname=csv.loc[i,'COLOR_NAME']
    return colorname


# In[8]:


def capture_camera_frame():
    TIMER = int(3)
    cap = cv2.VideoCapture(0) 
    while True: 
        ret, img = cap.read() 
        cv2.imshow('a', img) 
        k = cv2.waitKey(125) 
        if k == ord('s'): 
            prev= time.time() 
            while TIMER >= 0: 
                ret, img = cap.read() 
                font = cv2.FONT_HERSHEY_SIMPLEX 
                cv2.putText(img, str(TIMER), (200, 250), font,7, (0, 255, 255),4, cv2.LINE_AA) 
                cv2.imshow('a', img) 
                cv2.waitKey(125)
                cur = time.time()
                if cur-prev >= 1: 
                    prev= cur 
                    TIMER = TIMER-1
            else: 
                ret, img = cap.read()
                cv2.imshow('a', img)
                cv2.waitKey(2000)
                cv2.imwrite('camera.jpg', img) 
        elif k == 27: 
            break
    cap.release()
    cv2.destroyAllWindows()


# In[9]:


choice=0
acceptable_range=[1,2]
while choice not in acceptable_range:
    choice=int(input('press 1 if you want to find colors in a downloaded picture and press 2 if you want to find colors on a live video'))
    if choice not in acceptable_range:
        print('The entered value is unacceptable. please choose either 1 or 2')
if choice ==1:
    clicked=False
    img=pick_image()
    cv2.namedWindow('DETECTION')
    cv2.setMouseCallback('DETECTION',color_finder)
    while True:
        cv2.imshow("DETECTION",img)
        if clicked==True:
            cv2.rectangle(img,(10,10),(600,60),(b,g,r),-1)
            text= find_color_name(r,g,b)+' R='+ str(r)+' G='+ str(g)+' B='+str(b)
            cv2.putText(img,text,(50,50),2,0.8,(255,255,255),2,cv2.FONT_HERSHEY_COMPLEX)
            if(r+g+b>=600):
                cv2.putText(img,text,(50,50),2,0.8,(0,0,0),2,cv2.FONT_HERSHEY_COMPLEX)
            clicked=False 
        k=cv2.waitKey(10)
        if k & 0xFF ==27:
            break
    cv2.destroyAllWindows()
else:
    clicked=False
    capture_camera_frame()
    img= cv2.imread('camera.jpg')
    cv2.namedWindow('DETECTION')
    cv2.setMouseCallback('DETECTION',color_finder)
    while True:
        cv2.imshow("DETECTION",img)
        if clicked==True:
            cv2.rectangle(img,(10,10),(600,60),(b,g,r),-1)
            text= find_color_name(r,g,b)+' R='+ str(r)+' G='+ str(g)+' B='+str(b)
            cv2.putText(img,text,(50,50),2,0.8,(255,255,255),2,cv2.FONT_HERSHEY_COMPLEX)
            if(r+g+b>=600):
                cv2.putText(img,text,(50,50),2,0.8,(0,0,0),2,cv2.FONT_HERSHEY_COMPLEX)
            clicked=False 
        k=cv2.waitKey(10)
        if k & 0xFF ==27:
            break
    cv2.destroyAllWindows()


# In[ ]:





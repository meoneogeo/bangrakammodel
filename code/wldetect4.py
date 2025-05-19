#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 11:00:19 2021

@author: kampanartpiyathamrongchai
"""
# import picamera
from time import sleep
import numpy as np
import os
from datetime import datetime
# from matplotlib import pyplot as plt
import cv2 as cv
import random as rng
import imutils
import math
import requests


def calcDistance(x1,y1,x2,y2):
    dist = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1-y2), 2))
    #dist = math.sqrt(9)
    return dist


def calcWaterLevel(dist, slength, msl):
    wLevel = msl + ((slength-dist) * 202 / slength)
    return round(wLevel, 2)

def calcWaterLevel1(dist, slength, msl):
    wLevel = msl + ((dist * 202 / slength)/100)
    return round(wLevel, 2)

def stafflength(image):
    # Mask Dimension---------------------------
    
   
   
    # -- Closing Mophology
    kernel = np.ones((5,5),np.uint8)
    close1 = cv.morphologyEx(image,cv.MORPH_CLOSE,kernel, iterations = 10)
    
    # -- Opening Mophology
    kernel = np.ones((5,5),np.uint8)
    imgopen1 = cv.morphologyEx(close1, cv.MORPH_OPEN,kernel, iterations = 1)
    #cv.imshow('inputss', cv.resize(imgopen1, (680, 400)))
    
    min_val,max_val,min_indx,max_indx=cv.minMaxLoc(imgopen1)
    # print(min_val,max_val,min_indx,max_indx)
    
    ret, thresh = cv.threshold(imgopen1,max_val*1/5,255,cv.THRESH_BINARY)
    ret, thresh = cv.threshold(imgopen1,0,255,cv.THRESH_BINARY)
    

    canny_mask = cv.Canny(thresh,255,255)
    contours_mask = cv.findContours(canny_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #print(canny_mask.shape)
    cv.imshow("mask_cannyss", cv.resize(canny_mask, (680, 400)))
    
    cnts_mask = imutils.grab_contours(contours_mask)
    #print(len(cnts_mask))
    
    contours_mask_poly = [None]*len(cnts_mask)
    boundRect_mask = [None]*len(cnts_mask)
    
    # drawing_mask = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for i, c in enumerate(cnts_mask):
        contours_mask_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect_mask[i] = cv.boundingRect(contours_mask_poly[i])
    
    #print(boundRect_mask)
    staff_length = calcDistance(int(boundRect_mask[0][0]), int(boundRect_mask[0][1]), int(boundRect_mask[0][0]), int(boundRect_mask[0][1]+int(boundRect_mask[0][3])))
    print(staff_length)
    return staff_length

    # ----------------------------
    
# def sendWaterLevel(dtime, wlevel, imagename):
#     url = "https://www.geo-nred.nu.ac.th/nodejs/api/imageupload/collectdata"
#     data = {"data" : {"sid": "sta001", "dtime": dtime, "wlevel": wlevel, "image": imagename}}
#     requests.post(url = url, json=data)


# upload image URL
url = 'https://www.geo-nred.nu.ac.th/nodejs/api/imageupload/upload'
now = datetime.now()

# imgname = 'stat1_' + now.strftime("%d-%m-%Y-%H%M%S") + '.jpg'

# camera = picamera.PiCamera()
# camera.resolution = (1920, 1080)
# camera.start_preview()
# sleep(0.5)

# camera.capture(imgname)
# camera.stop_preview()
# camera.close()


image_noflood = '/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/code/stat01_noflood.jpeg'
image_sample = '/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/code/stat01_flood_131122.jpeg'
image_mask = '/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/code/stat01_zmask.jpg'
# staff_length = 329.

img0 = cv.imread(image_sample, cv.IMREAD_GRAYSCALE)
img_noflood = cv.imread(image_noflood, cv.IMREAD_GRAYSCALE)
imgbgr = cv.imread(image_sample)
mask = cv.imread(image_mask, 0)

#cv.imshow('input0', img0)
#img1 = cv.equalizeHist(img0)
img1 = img0
output = imgbgr.copy()

ret, maskthresh = cv.threshold(mask,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
#cv.imshow('input0', maskthresh)
#print(maskthresh.shape)

#--Masking image with 0 and 255 masked image
mask2 = (maskthresh == 255)
imgMask0 = np.copy(maskthresh)
imgNoFloodMask = np.copy(maskthresh)
imgMask0[mask2] = img1[mask2]
imgNoFloodMask[mask2] = img_noflood[mask2]


#imgMask = cv.equalizeHist(imgMask0)
imgMask1 = imgMask0
#cv.imshow('inputm', cv.resize(imgNoFloodMask, (680, 400)))
#cv.imshow('inputs', cv.resize(imgMask1, (680, 400)))


# -- Calculate length of no flood staff
staff_length = stafflength(mask)
# staff_length = 336.
print(staff_length)

# -- Closing Mophology
kernel = np.ones((3,3),np.uint8)
close = cv.morphologyEx(imgMask1,cv.MORPH_CLOSE,kernel, iterations = 1)
#close = cv.equalizeHist(close0)
cv.imshow('close', cv.resize(close, (680, 400)))

kernel2 = np.ones((3, 3), np.float32)/9



# -- Opening Mophology
kernel = np.ones((5,5),np.uint8)
imgopen0 = cv.morphologyEx(close, cv.MORPH_OPEN,kernel, iterations = 9)
cv.imshow('open', cv.resize(imgopen0, (680, 400)))

# Applying the filter2D() function
imgopen = cv.filter2D(src=imgopen0, ddepth=-1, kernel=kernel2)
cv.imshow('filt', cv.resize(imgopen, (680, 400)))




min_val,max_val,min_indx,max_indx=cv.minMaxLoc(imgopen)
print(min_val,max_val,min_indx,max_indx)


if max_val-min_val <120:
    mul = 99/100
else:
    mul = 4.5/5

ret, thresh = cv.threshold(imgopen,max_val*mul,max_val,cv.THRESH_BINARY)
#cv.imshow("shift", cv.resize(thresh, (680, 400)))

canny_output = cv.Canny(thresh,255,255)
contours = cv.findContours(canny_output.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# print(canny_output.shape)
cv.imshow("BG", cv.resize(canny_output, (680, 400)))

cnts = imutils.grab_contours(contours)
# print(cnts)

cnts1 = []

for i, c in enumerate(cnts):
    area = cv.contourArea(c)
    print(area)
    if area > 0.5:
        cnts1.append(c)

# contours_poly = [None]*len(cnts1)
# boundRect = [None]*len(cnts1)

# drawing = np.zeros((img1.shape[0], img1.shape[1], 3), dtype=np.uint8)
# for i, c in enumerate(cnts1):
#     contours_poly[i] = cv.approxPolyDP(c, 3, True)
#     boundRect[i] = cv.boundingRect(contours_poly[i])

# print(boundRect)
    
# color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
# # cv.drawContours(drawing, contours_poly, 2, color)
# ((x, y), _) = cv.minEnclosingCircle(cnts1[0])
# # cv.rectangle(drawing, (int(boundRect[2][0]), int(boundRect[2][1])), (int(boundRect[2][0]+boundRect[2][2]), int(boundRect[2][1]+boundRect[2][3])), color, 2)

# cv.line(drawing, (0, int(boundRect[0][1]+boundRect[0][3])), (int(boundRect[0][0])+381,int(boundRect[0][1]+boundRect[0][3])), (0,0,255), 3)
# dist = calcDistance(int(boundRect[0][0]), int(boundRect[0][1]), int(boundRect[0][0]), int(boundRect[0][1]+int(boundRect[0][3])))

# print(dist)
# cv.putText(output, "Water Level: #{}".format(calcWaterLevel(dist, staff_length)), (int(x) - 100, int(boundRect[0][1]+int(boundRect[0][3])) + 20),cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

# cv.addWeighted(drawing, 0.5, output, 1 - 0.5,0, output)
# cv.imshow("line", output)

if len(cnts1) != 0:
    contours_poly = [None]*len(cnts1)
    boundRect = [None]*len(cnts1)
    
    drawing = np.zeros((img1.shape[0], img1.shape[1], 3), dtype=np.uint8)
    for i, c in enumerate(cnts1):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
    
    print(boundRect)
        
    color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    # cv.drawContours(drawing, contours_poly, 2, color)
    ((x, y), _) = cv.minEnclosingCircle(cnts1[0])
    # cv.rectangle(drawing, (int(boundRect[2][0]), int(boundRect[2][1])), (int(boundRect[2][0]+boundRect[2][2]), int(boundRect[2][1]+boundRect[2][3])), color, 2)
    
    #cv.line(drawing, (0, int(boundRect[0][1]+boundRect[0][2])), (int(boundRect[0][0])+500,int(boundRect[0][1]+boundRect[0][2])), (0,0,255), 3)
    cv.line(drawing, (0, int(boundRect[0][1])), (int(boundRect[0][0])+500,int(boundRect[0][1])), (0,0,255), 3)
    dist = calcDistance(int(boundRect[0][0]), int(boundRect[0][1]), int(boundRect[0][0]), int(boundRect[0][1]+int(boundRect[0][3])))
    
    print(dist)
    cv.putText(output, "Water Level: #{}".format(calcWaterLevel1(dist, staff_length, 40.7)), (int(x) + 200, int(boundRect[0][1]) - 10),cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    print(calcWaterLevel1(dist, staff_length, 0))
    
    cv.addWeighted(drawing, 0.8, output, 1 - 0.5,0, output)
    cv.imshow("line", output)
    cv.imwrite('output.jpg', output)
    # sendWaterLevel(now.strftime("%d-%m-%Y-%H%M%S"), calcWaterLevel(dist, staff_length), imgname)
    
    
else:
    
    drawing = np.zeros((img1.shape[0], img1.shape[1], 3), dtype=np.uint8)
            
    color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    # cv.drawContours(drawing, contours_poly, 2, color)
    ((x, y), _) = cv.minEnclosingCircle(cnts1[0])
    # cv.rectangle(drawing, (int(boundRect[2][0]), int(boundRect[2][1])), (int(boundRect[2][0]+boundRect[2][2]), int(boundRect[2][1]+boundRect[2][3])), color, 2)
    
    cv.line(drawing, (0, int(boundRect[0][1]+boundRect[0][3])), (int(boundRect[0][0])+381,int(boundRect[0][1]+boundRect[0][3])), (0,0,255), 3)
    dist = calcDistance(int(boundRect[0][0]), int(boundRect[0][1]), int(boundRect[0][0]), int(boundRect[0][1]+int(boundRect[0][3])))
    
    print(dist)
    cv.putText(output, "Water Level: #{}".format(calcWaterLevel1(0, staff_length, 40.7)), (int(x) - 100, int(boundRect[0][1]+int(boundRect[0][3])) + 20),cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    
    cv.addWeighted(drawing, 0.8, output, 1 - 0.5,0, output)
    cv.imshow("line", output)
    cv.imwrite('output.jpg', output)
    # sendWaterLevel(now.strftime("%d-%m-%Y-%H%M%S"), calcWaterLevel(0, staff_length), imgname)


# # #Send Image to Server
# with open(imgname, 'rb') as img:
#     name_img = os.path.basename(imgname)
#     files = {'image' : (name_img,img, 'multipart/form-data', {'Expires' : '0'} )}
#     with requests.Session() as s:
#         r = s.post(url, files=files);
#         print(r.status_code)

# os.remove(imgname)
#os.remove(imgname)



cv.waitKey(1)
cv.destroyAllWindows() 
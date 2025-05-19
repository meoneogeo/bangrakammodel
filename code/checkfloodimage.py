#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:58:46 2022

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

#==แก้ตรงนี้
def calcWaterLevel(dist, slength, msl):     
    wLevel = msl + ((slength-dist) * 200 / slength)
    return round(wLevel, 2)

def stafflength(image):
    # Mask Dimension---------------------------
    
   
   
    # -- Closing Mophology
    kernel = np.ones((5,5),np.uint8)
    close1 = cv.morphologyEx(image,cv.MORPH_CLOSE,kernel, iterations = 3)
    
    # -- Opening Mophology
    kernel = np.ones((5,5),np.uint8)
    imgopen1 = cv.morphologyEx(close1, cv.MORPH_OPEN,kernel, iterations = 6)
#     cv.imshow('input', cv.resize(imgopen1, (680, 400)))
    
    min_val,max_val,min_indx,max_indx=cv.minMaxLoc(imgopen1)
    # print(min_val,max_val,min_indx,max_indx)
    
    ret, thresh = cv.threshold(imgopen1,max_val*2/5,255,cv.THRESH_BINARY) #==แก้ตรงนี้
    

    canny_mask = cv.Canny(thresh,255,255)
    contours_mask = cv.findContours(canny_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    print(canny_mask.shape)
#     cv.imshow("mask_canny", cv.resize(canny_mask, (680, 400)))
    
    cnts_mask = imutils.grab_contours(contours_mask)
    print(len(cnts_mask))
    
    contours_mask_poly = [None]*len(cnts_mask)
    boundRect_mask = [None]*len(cnts_mask)
    
    # drawing_mask = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for i, c in enumerate(cnts_mask):
        contours_mask_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect_mask[i] = cv.boundingRect(contours_mask_poly[i])
    
    print(boundRect_mask)
    staff_length = calcDistance(int(boundRect_mask[0][0]), int(boundRect_mask[0][1]), int(boundRect_mask[0][0]), int(boundRect_mask[0][1]+int(boundRect_mask[0][3])))
    print(staff_length)
    return staff_length

    # ----------------------------
    
def sendWaterLevel(dtime, wlevel, imagename):
    url = "https://www.geo-nred.nu.ac.th/nodejs/api/imageupload/collectdata"
    data = {"data" : {"sid": "sta001", "dtime": dtime, "wlevel": wlevel, "image": imagename}}
    requests.post(url = url, json=data)



image_noflood = '/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/code/stat2_noflood.jpg'
image_sample = '/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/code/stat2_noflood.jpg'
image_mask = '/Users/kampanartpiyathamrongchai/MyDoc/2564/project/irri/code/stat2_mask.jpg'
# staff_length = 329.

img0 = cv.imread(image_sample, cv.IMREAD_GRAYSCALE)
img_noflood = cv.imread(image_noflood, cv.IMREAD_GRAYSCALE)
imgbgr = cv.imread(image_sample)
mask = cv.imread(image_mask, 0)

cv.imshow('input0', img0)
# img1 = cv.equalizeHist(img0)
img1 = img0
output = imgbgr.copy()

ret, maskthresh = cv.threshold(mask,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
cv.imshow('input0', maskthresh)
print(maskthresh.shape)

#--Masking image with 0 and 255 masked image
mask2 = (maskthresh == 255)
imgMask0 = np.copy(maskthresh)
imgNoFloodMask = np.copy(maskthresh)
imgMask0[mask2] = img1[mask2]
imgNoFloodMask[mask2] = img_noflood[mask2]


# imgMask = cv.equalizeHist(imgMask0)
imgMask1 = imgMask0
cv.imshow('input', cv.resize(imgNoFloodMask, (680, 400)))



cv.waitKey(1)
cv.destroyAllWindows() 







# -*- coding: utf-8 -*-
import numpy as np
import potrace
import cv2 
#Our libraries:
from myimage import *




##############################################################
# Load image

img = myimage("images/monk.jpg")
img.display()

'''
# Create a bitmap from the array
bmp = potrace.Bitmap(data)
# Trace the bitmap to a path
path = bmp.trace(turdsize = 0 ,turnpolicy = potrace.TURNPOLICY_MINORITY,opticurve = 0, alphamax=0, opttolerance = 100)


# Iterate over path curves

img = np.zeros((height+1,width+1,1), np.uint8)
img.fill(255)


img2 = np.zeros((height+1,width+1,1), np.uint8)
img2.fill(255)

for i,curve in enumerate(path):
    if(i == 0):
        continue
    x1,y1 =  curve.start_point

    x1 = int(x1)
    y1 = int(y1)
    
    img2[y1,x1] = 0
    
    for segment in curve:
        x2,y2 = segment.end_point


        
        x2 = int(x2)
        y2 = int(y2)
        
        img2[y2,x2] = 0


        lineThickness = 1
        cv2.line(img, (x1,y1), (x2,y2), 0, lineThickness)
        x1 = x2
        y1 = y2
        

cv2.imshow('Points', img2 )
cv2.waitKey(0)
cv2.destroyAllWindows()
      
        

cv2.imshow('Lines', img )
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
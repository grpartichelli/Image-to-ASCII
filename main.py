# -*- coding: utf-8 -*-
import numpy as np
import potrace
import cv2 
#Our libraries:
from myimage import *
from character import *
##############################################################

# Load image
img = myimage("images/monk.jpg")
'''
img.display()
img.display_points()
img.display_lines()
'''

for i in range(33,127):
    char = character(i)
    char.display()
    

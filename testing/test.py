import sys 
sys.path.insert(1,'..')

# -*- coding: utf-8 -*-
import numpy as np
import cv2 
from scipy.spatial.distance import cdist, cosine
from scipy.optimize import linear_sum_assignment

#Our libraries:
from myimage import *
from character import *
import math



def show_points(img):
	points = img.points
	img = np.zeros((img.height+1,img.width+1,1), np.uint8)
	#img.fill()
	#Draw all the lines
	for point in points:
		img[point[1],point[0]] = 255
		

	cv2.imshow('Points', img )
	cv2.waitKey(0)
	cv2.destroyAllWindows()




img = myimage("../big_characters/100.png")
show_points(img)

descriptor = get_descriptor(img)


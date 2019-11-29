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


img = myimage("../images/monk.jpg")
#show_points(img)
points = img.points


##############################Passo 2#####################################

npoints = len(points)
# distance
r_array = cdist(points, points) #Compute distance between each pair of the two collections of inputs.


# Getting two points with maximum distance to norm angle by them
# this is needed for rotation invariant feature
max_dist = r_array.argmax() #Gets the biggest distance between two points
max_points = [max_dist / npoints, max_dist % npoints] 

# Normalizing
r_array_n = r_array / r_array.mean() #The .mean() returns the average of the array elements. 


##############################Passo 3#####################################
#Used to create log scale
nbins_r=5
r_inner=0.1250
r_outer=2.0

#Creating log_scale [0.125 0.25  0.5   1.    2.   ]
log_space = np.logspace(np.log10(r_inner), np.log10(r_outer), nbins_r)

#Creating empty array of points
r_array_q = np.zeros((npoints, npoints), dtype=int)

#Counting for every normalized distance, how many times it is smaller than the numbers on the log scale (Quantization process)
#Ex: True+True in python equals 2, while False+Flase equals 0. True+False equals 1 etc...
#The higher the number on r_array_q, the closer the points are!
for i in range(nbins_r):
    r_array_q += (r_array_n < log_space[i])



######################################PASSO 4###########################################



#The theta_array is the angle between every point (considering they are lines with one point at the origin)
theta_array = cdist(points, points, lambda u, v: math.atan2((v[1] - u[1]), (v[0] - u[0])))

#We normalize them using norm_angle 
norm_angle = theta_array[int(max_points[0]),max_points[1]]

# making angles matrix rotation invariant
negative_identity_matrix = np.ones((npoints, npoints)) - np.identity(npoints)
theta_array = (theta_array - norm_angle * negative_identity_matrix )

# removing all very small values because of float operation
theta_array[np.abs(theta_array) < 1e-7] = 0

# 2Pi shifted because we need angels in [0, 2Pi]
theta_array = theta_array + 2 * math.pi * (theta_array < 0)

######################################PASSO 5###########################################
nbins_theta=12

#Quantize our angles to get histogram the same as for distance
#Basically divides the array by 2pi/nbins_theta, adds 1 (it rounds it down first)
theta_array_q = (1 + np.floor(theta_array/ (2 * math.pi / nbins_theta))).astype(int)

######################################PASSO 6###########################################
#Get all things together and build shape context descriptor. Just counting number of points in each radius and angle region.


import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)




#To get only values bigger than zero
fz = r_array_q > 0
#Declare the descriptor
nbins = nbins_theta * nbins_r
descriptor = np.zeros((npoints, nbins))


for i in range(npoints):
    sn = np.zeros((nbins_r, nbins_theta))
    for j in range(npoints):
    	#For each two points, if their r_array_q isnt 0
    	if (fz[i, j]):
           sn[r_array_q[i, j] - 1, theta_array_q[i, j] - 1] += 1
    descriptor[i] = sn.reshape(nbins)

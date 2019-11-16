# -*- coding: utf-8 -*-
import numpy as np
import potrace
import cv2 
#Our libraries:
from myimage import *
from character import *
##############################################################
def transform_image(blocks):
	for i,line in enumerate(blocks):
		for j,block in enumerate(line):
			#Concatenating the blocks to create a line
			if j == 0:
				block_line = block				
			else:
				block_line = np.concatenate((block_line, block), axis=1)

		#Concatenating the lines to create an image
		if i == 0:
			block_img = block_line
		else:
			block_img = np.concatenate((block_img, block_line), axis=0)

	return block_img
##############################################################

# Load image
img = myimage("images/monk.jpg")
img.display_lines()

#Load characters
chr_lst= []
for i in range(32,127):
    char = character(i)
    chr_lst.append(char)


#Gets the resolution of one of the characters(they are all the same)
chr_height,chr_width = char.size()

#Calculates the split image, its a list matrix with every block of the image
blocks = img.split_up(chr_height,chr_width)
#Transform a matrix of blocks into an image
block_img = transform_image(blocks)
				



cv2.imshow('Image', block_img)
cv2.waitKey(0)
cv2.destroyAllWindows()



'''
for char in chr_lst:
	print(char.get_img())
'''
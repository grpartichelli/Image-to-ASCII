# -*- coding: utf-8 -*-
import cv2 
from skimage.measure import find_contours, approximate_polygon, subdivide_polygon
from skimage import measure
import numpy as np

class character():
	symbol = None 
	number = None
	img = None
	def __init__(self,char_number):
		self.number = char_number
		self.symbol = chr(char_number)
		img_temp = cv2.imread("big_characters/" + str(char_number) + ".png",0)
		#Convert img to black and white
		thresh,img_temp = cv2.threshold(img_temp, 200, 255, cv2.THRESH_BINARY)
		self.img = img_temp
		self.points =None
	

	def get_symbol(self):
		return self.symbol

	def get_number(self):
		return self.number

	def get_img(self):
		return self.img

	def get_points(self):
		return self.points

	#Displays the image
	def display(self):
		cv2.imshow('Image', self.img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def size(self):
		return  self.img.shape
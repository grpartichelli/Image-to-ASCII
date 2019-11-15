import numpy as np
import potrace
import cv2 

class myimage():
	
	img= None;
	bmp= None;
	height = None;
	shape = None;

	def __init__(self, image_path):
		img = cv2.imread(image_path,0)
		self.height, self.width = img.shape
		
		#Turn image to black and white
		ret,self.img = cv2.threshold(img, 80, 255, 0)
		self.bmp = self.img/255

	#Displays the non-bmp image
	def display(self):
		cv2.imshow('Image', self.img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
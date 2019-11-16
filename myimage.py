import numpy as np
import potrace
import cv2 

class myimage():
	img= None; #Black and white version of the image
	bmp= None; #Bit map version of the image
	height = None; #Image height
	width = None;  #Image width
	
	lines= [];  #All the lines of the image
	lines_img= None #Image of the lines

	split_img = [] #Matrix with all the blocks of character sizes

	def __init__(self, image_path):
		img = cv2.imread(image_path,0)

		
		#This code adds a white padding around the image
		#The padding helps separete contours from the borders and allows us to ignore the borders when dividing the image
		top, bottom, left, right = [25]*4 #25 is the size of the padding
		img= cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255,255,255])

		#Gets the image shape
		self.height, self.width = img.shape
		
		#Turn image to black and white
		ret,self.img = cv2.threshold(img, 80, 255, 0)
		self.bmp = self.img/255

		self.lines = self.get_lines()
		self.lines_img =self.get_lines_img(2)
		


	#Get the lines of the image
	def get_lines(self):
	# Trace the bitmap to a path
		path = potrace.Bitmap(self.bmp).trace()
		lines = []
		#Get all the lines on the image 
		for i,curve in enumerate(path):
			if(i == 0):
				continue
			
			x1,y1 =  curve.start_point
			x1 = int(x1)
			y1 = int(y1)
			for segment in curve:
				x2,y2 = segment.end_point
				x2 = int(x2)
				y2 = int(y2)

				lines.append(((x1,y1),(x2,y2)))
				
				x1 = x2
				y1 = y2
				
		return lines



	#Return the image with the drawn lines
	def get_lines_img(self,line_thickness):
		#Creates an empty image
		img = np.zeros((self.height+1,self.width+1,1), np.uint8)
		img.fill(255)

		#Draw all the lines
		for line in self.lines:
			start_point = line[0]
			end_point = line[1]
			cv2.line(img, start_point,end_point, 0, line_thickness)
		
		return img


	#Displays the non-bmp image
	def display(self):
		cv2.imshow('Image', self.img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()


	def display_lines(self):
		cv2.imshow('Lines', self.lines_img )
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		

	def display_points(self):
		#Creates an empty image
		img = np.zeros((self.height+1,self.width+1,1), np.uint8)
		img.fill(255)

		#Draw all the lines
		for line in self.lines:
			start_point = line[0]
			end_point = line[1]
			#I dont understand why this is reverse
			img[start_point[1],start_point[0]] = 0
			img[end_point[1],end_point[0]] = 0 
		
		cv2.imshow('Points', img )
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return img


	def split_up(self,ch_height,ch_width):
		block_img = np.zeros((ch_height,ch_width))
		

		#Iterating over blocks
		for row in np.arange(self.height - ch_height + 1, step = ch_height):
			aux_list = []
			for col in np.arange(self.width - ch_width + 1, step = ch_width):
				block_img = self.lines_img[row:row+ch_height , col:col+ch_width]
				aux_list.append(block_img)

			self.split_img.append(aux_list)

		return self.split_img

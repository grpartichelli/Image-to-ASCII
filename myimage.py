import numpy as np
import potrace
import cv2 

class myimage():
	img= None; #Black and white version of the image
	bmp= None; #Bit map version of the image
	lines_img= None #Image of the lines
	height = None;
	shape = None;
	lines= [];

	def __init__(self, image_path):
		img = cv2.imread(image_path,0)
		self.height, self.width = img.shape
		
		#Turn image to black and white
		ret,self.img = cv2.threshold(img, 80, 255, 0)
		self.bmp = self.img/255

		self.lines = self.get_lines()
		self.lines_img =self.get_lines_img(1)
	

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
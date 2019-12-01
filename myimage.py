import numpy as np
import cv2 
from skimage import measure

from skimage.measure import find_contours, approximate_polygon, subdivide_polygon
from PIL import Image
import potrace

DEF_WIDTH = 700
DEF_HEIGHT = 700

class myimage():
    img= None; #Black and white version of the image
    bmp= None; #Bit map version of the image
    height = None; #Image height
    width = None;  #Image width
    
    lines= [];  #All the lines of the image
    lines_img= None #Image of the lines

    split_img = [] #Matrix with all the blocks of character sizes

    line_thickness = 5

    def __init__(self, image_path):
        img = cv2.imread(image_path,0)


        #This code adds a white padding around the image
        #The padding helps separete contours from the borders and allows us to ignore the borders when dividing the image
        top, bottom, left, right = [25]*4 #25 is the size of the padding
        img= cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255,255,255])

        #Gets the image shape
        self.height, self.width = img.shape

        ratio_h =  DEF_HEIGHT/self.height
        ratio_w =  DEF_WIDTH/self.width

        img = cv2.resize(img,None,fx=ratio_w,fy=ratio_h)
        
        self.height = DEF_HEIGHT
        self.width = DEF_WIDTH
        

        #Turn image to black and white
        ret,self.img = cv2.threshold(img, 65, 255, 0)
        self.bmp = self.img/255

        self.lines,self.points = self.calculate_lines_and_points()

        self.lines_img =self.get_lines_img(self.line_thickness)
        


   #Get the lines and points of the image
    def calculate_lines_and_points(self):
    # Trace the bitmap to a path
        
        contours = measure.find_contours(self.img, level = 1)
        lines = []
        points = []
        #Get all the lines on the image 
        for contour in contours:
            
            for i,point in enumerate(approximate_polygon(contour, tolerance=2)):
                
                y2,x2 = int(point[0]),int(point[1])
                points.append([x2,y2])
                if i != 0:
                    lines.append(((x1,y1),(x2,y2)))
                
                x1,y1 = x2,y2
                
        
        return lines,points



    #Return the image with the drawn lines
    def get_lines_img(self,line_thickness):
        #Creates an empty image
        img = np.zeros((self.height+1,self.width+1))
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
        points = self.points
        img = np.zeros((self.height+1,self.width+1,1), np.uint8)
        #img.fill()
        #Draw all the lines
        for point in points:
            img[point[1],point[0]] = 255
            

        cv2.imshow('Points', img )
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #Creates a list matrix of every block of the image

    def split_up(self,ch_height,ch_width):
        block = np.zeros((ch_height,ch_width))
        self.split_img = []

        #Iterating over blocks
        for row in np.arange(self.height - ch_height + 1, step = ch_height):
            count =0
            for col in np.arange(self.width - ch_width + 1, step = ch_width):
                count = count + 1
                block = self.img[row:row+ch_height , col:col+ch_width]
                
                self.split_img.append(block)
                if col == 0 and row == 0:
                    pass

            
        
        return self.split_img,count

                
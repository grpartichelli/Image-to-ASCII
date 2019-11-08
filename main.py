import numpy as np
import cv2 
import matplotlib.pyplot as plt
from skimage import measure


#Cria uma imagem e coloca nela os pixeis que são os vertexes das linhas que formam os
#contours
def draw_points(contours,height,width):
    
    img = np.zeros((height,width,1), np.uint8)
    img.fill(255)

    for line in contours:
        for point in line:
            point = point[0]
            #Os pontos ficam dentro de um array?
            #Tipo: [[22,33]]
            img[point[1],point[0]] = 0

    cv2.imshow('Points', img )
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#Pinta os contours na imagem
def draw_contours(contours,height,width):
    
    img = np.zeros((height,width,1), np.uint8)
    img.fill(255)
    cv2.drawContours(img, contours, -1, 0,1)
    
    cv2.imshow('Contours', img )
    cv2.waitKey(0)
    cv2.destroyAllWindows()


##############################################################
# Load image
img = cv2.imread('images/triangle.png',0)
#Turn image to black and white
ret,img = cv2.threshold(img, 80, 255, 0)
#Get image height and width
height, width = img.shape


cv2.imshow('Image', img )
cv2.waitKey(0)
cv2.destroyAllWindows()


#############################################################
#Getting the contours
contours,hierarchy= cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE )


draw_contours(contours,height,width)
draw_points(contours,height,width)




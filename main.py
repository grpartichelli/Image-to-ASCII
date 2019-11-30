# -*- coding: utf-8 -*-
import numpy as np
import cv2 
from scipy.spatial.distance import cdist, cosine
from scipy.optimize import linear_sum_assignment
from skimage.measure import find_contours, approximate_polygon, subdivide_polygon
#Our libraries:
from myimage import *
from character import *
import math

def display_points(img):
        points = calculate_points(img)
        height,width = img.shape
        img = np.zeros((height+1,width+1,1), np.uint8)
        #img.fill()
        #Draw all the lines
        for point in points:
            img[point[1],point[0]] = 255
            

        cv2.imshow('Points', img )
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #Creates a list matrix of every block of the image


 #Get the lines and points of the image
def calculate_points(img):
# Trace the bitmap to a path
    
    contours = measure.find_contours(img, level = 1)
    lines = []
    points = []
    #Get all the lines on the image 
    for contour in contours:
        
        for i,point in enumerate(approximate_polygon(contour, tolerance=2)):
            
            y2,x2 = int(point[0]),int(point[1])
            points.append([x2,y2])
            
            
    
    return points




#Calculate the SHAPE DESCRIPTOR of the image
def get_descriptor(points):

    if points == []:
        points = [[0,0],[0,1]]
    #Used to create log scale, quantisize the point distance
    nbins_r=5
    r_inner=0.1250
    r_outer=2.0
    #Used to quantisize the angles
    nbins_theta=12


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
    

    #Quantize our angles to get histogram the same as for distance
    #Basically divides the array by 2pi/nbins_theta, adds 1 (it rounds it down first)
    theta_array_q = (1 + np.floor(theta_array/ (2 * math.pi / nbins_theta))).astype(int)

    ######################################PASSO 6###########################################
    #Get all things together and build shape context descriptor. Just counting number of points in each radius and angle region.

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
    return descriptor

##############################################################
#Function returns a value which is used to compare a block with a character

def compare_function(block,character):
    return np.average(abs(character.get_img() - block))

def get_best_characters(blocks,char_list):

    characters= []
    for block in blocks:
        value = 100000000000
        for character in char_list:
            #Finds the minimum value for this value, that will be our character.
            temp_value = compare_function(block,character)

            if temp_value < value:
                value = temp_value
                best_character = character

            if value == 0:
                break
        
        characters.append(best_character)       
            
        
    return characters


'''
#Finds the best character for each block
def get_best_characters(blocks,char_list):
    best_characters = []


    chr_descs = []
    for character in char_list:
        chr_points = calculate_points(character.get_img())
        chr_descs.append(get_descriptor(chr_points))

    chr_descs = np.array(chr_descs)   
    
    block_descs = [] 
    for block in blocks:
        block_descs.append(get_descriptor(calculate_points(block)))
    
    block_descs = np.array(block_descs)        
    
   
    for desc in block_descs:
        distances = []
        for chr_desc in chr_descs:
            dist = cdist(chr_desc, desc, metric="cosine")
            distances.append(dist.mean())

        character = char_list[distances.index(min(distances))]
        best_characters.append(character)
   
    return best_characters
 '''   
##############################################################
#Transform a matrix of characters into an image
def characters_to_image(characters, blocks_per_line):
    count = 0
    first_row = True

    for character in characters:
        count = count + 1
        if count == 1:
            character_row= character.get_img()          
        else:
            character_row = np.concatenate((character_row, character.get_img()), axis=1)


        if count == blocks_per_line:
            if first_row:
                character_img = character_row
                first_row = False
            else:
                character_img  = np.concatenate((character_img, character_row), axis=0)
            count = 0 

    return character_img 
##############################################################
#Writes a list matrix of characters into a file
def write_characters(filename,characters,blocks_per_line):
    #Writes the characters on a txt file
    f = open(filename, "w")
    count = 0

    for character in characters:
        count = count + 1
        f.write(character.get_symbol())
        
        if count == blocks_per_line:
            count = 0
            f.write("\n")
    f.close()

############################################################################################################################


def main():

    # Load image
    img = myimage("images/monk.jpg")
    img.display()
    img.display_lines()
    
    #Load characters
    char_list= []
    for i in range(32,127):
        char = character(i)
        char.points = calculate_points(char.get_img())
        char_list.append(char)
      




    #Gets the resolution of one of the characters(they are all the same)
    chr_height,chr_width = char.size()

    #Calculates the split image, its a list matrix with every block of the image
    blocks,blocks_per_line= img.split_up(chr_height,chr_width)


    #Gets the best characters
    best_characters = get_best_characters(blocks,char_list)
    write_characters("output.txt",best_characters,blocks_per_line)

    #Transform a matrix of blocks into an image
    character_img = characters_to_image(best_characters,blocks_per_line)
            
    cv2.imshow('Image', character_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    

if __name__ == "__main__":
    main()



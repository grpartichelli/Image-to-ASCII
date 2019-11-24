# -*- coding: utf-8 -*-
import numpy as np
import cv2 
#Our libraries:
from myimage import *
from character import *


##############################################################
#Function returns a value which is used to compare a block with a character
def compare_function(block,character):
	return np.average(abs(character.get_img() - block))

#Finds the best character for each block
def get_best_characters(blocks,char_list):

	characters= []
	for line in blocks:
		character_line = []
		for block in line:
			value = 10000000000
			
			for character in char_list:
				#Finds the minimum value for this value, that will be our character.
				temp_value = compare_function(block,character)

				if temp_value < value:
					value = temp_value
					best_character = character

				if value == 0:
					break
				
					
			character_line.append(best_character)
		characters.append(character_line)
	return characters
##############################################################
#Transform a matrix of characters into an image
def characters_to_image(characters):
	for i,character_line in enumerate(characters):
		for j,character in enumerate(character_line):
			#Concatenating the blocks to create a line
		
			if j == 0:
				character_row= character.get_img()			
			else:
				character_row = np.concatenate((character_row, character.get_img()), axis=1)

		#Concatenating the lines to create an image
		if i == 0:
			character_img = character_row
		else:
			character_img  = np.concatenate((character_img, character_row), axis=0)

	return character_img 
##############################################################
#Writes a list matrix of characters into a file
def write_characters(filename,characters):
	#Writes the characters on a txt file
	f = open(filename, "w")

	for line in characters:
		for character in line:	
			f.write(character.get_symbol())
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
	    char_list.append(char)


	#Gets the resolution of one of the characters(they are all the same)
	chr_height,chr_width = char.size()

	#Calculates the split image, its a list matrix with every block of the image
	blocks = img.split_up(chr_height,chr_width)

	#Gets the best characters
	best_characters = get_best_characters(blocks,char_list)

	#Transform a matrix of blocks into an image
	character_img = characters_to_image(best_characters)
			
	cv2.imshow('Image', character_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


	write_characters("output.txt",best_characters)

if __name__ == "__main__":
	main()



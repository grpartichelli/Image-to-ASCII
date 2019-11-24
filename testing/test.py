import sys 
sys.path.insert(1,'..')

# -*- coding: utf-8 -*-
import numpy as np
import cv2 
#Our libraries:
from myimage import *
from character import *



from skimage.transform import warp_polar
img = myimage("../images/monk.jpg")
img = img.img

img  = warp_polar(img, scaling='log')

cv2.imshow('Points', img )
cv2.waitKey(0)
cv2.destroyAllWindows()

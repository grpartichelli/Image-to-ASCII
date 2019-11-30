from scipy.spatial.distance import cdist, cosine
from scipy.optimize import linear_sum_assignment
import math


class descriptor():

	def __init___(self,image):
		#Used to create log scale for point difference
		nbins_r=5
		r_inner=0.1250
		r_outer=2.0
		#Bins for angle difference
		nbins_theta=12
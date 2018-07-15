# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

import cv2
import os
import imutils
from skimage.feature import hog
from skimage import exposure

path ="DataBase\\Nodule_x1\\Diagx1\\"
path2 = "Imagens_teste\\"
#path3 = "D:\\Bases\\Pulmao\\LUNA_raissa\\Luna_worked\\Cortes_jpg\\Nodule\\Diagx1\\"
images = os.listdir(path)

for im_file in images:
	im_path = path + im_file
	print im_path

	im = cv2.imread(im_path)
	# redimencionar a imagem para ter uma proporção 1x2
	resized_image = imutils.resize(im, width=80, height=80)

	fd, hog_image = hog(resized_image, orientations=8, pixels_per_cell=(16, 16),cells_per_block=(1, 1), visualize=True)

	# Rescale histogram for better display
	hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

	cv2.imshow('hog', hog_image_rescaled)
	cv2.imshow('original', im)
	cv2.waitKey(0)
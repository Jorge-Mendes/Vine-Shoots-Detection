#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import sys
import glob

from termcolor import colored    # to print colored text in terminal

#Drag rectangle from top left to bottom right
#https://www.learnopencv.com/how-to-select-a-bounding-box-roi-in-opencv-cpp-python/

clear = lambda: os.system('clear')
clear()

cropping = False
 
x_start, y_start, x_end, y_end = 0, 0, 0, 0

greater_than_10_input_path = "dataset/whole_images/greater_than_10/"
smaller_than_10_input_path = "dataset/whole_images/smaller_than_10/"

greater_than_10_output_path = "dataset/cropped_images/greater_than_10/"
smaller_than_10_output_path = "dataset/cropped_images/smaller_than_10/"

greater_than_10_images_class = "greater_than_10"
smaller_than_10_images_class = "smaller_than_10"

greater_than_10_last_image = 1
smaller_than_10_last_image = 1

def getListOfFiles(dirName):
	# create a list of file and sub directories 
	# names in the given directory 
	listOfFile = sorted(os.listdir(dirName))
	allFiles = list()
	# Iterate over all the entries
	for entry in listOfFile:
		# Create full path
		fullPath = os.path.join(dirName, entry)
		# If entry is a directory then get the list of files in this directory 
		if os.path.isdir(fullPath):
			allFiles = allFiles + getListOfFiles(fullPath)
		else:
			allFiles.append(fullPath)
                
	return allFiles
	# Source: https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/


imglist = getListOfFiles(smaller_than_10_input_path)
#print imglist

roi = []

#index = 1

#=================================#
#=== GET THE LAST IMAGE NUMBER ===#
#=================================#
def verify_dataset():
	global greater_than_10_last_image
	global smaller_than_10_last_image
	greater_than_10_last_image = 1
	smaller_than_10_last_image = 1
	if greater_than_10_last_image <= 9:
		while glob.glob(greater_than_10_output_path + "greater_than_10__0000%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	if greater_than_10_last_image > 9 and greater_than_10_last_image <= 99:
		while glob.glob(greater_than_10_output_path + "greater_than_10__000%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	if greater_than_10_last_image > 99 and greater_than_10_last_image <= 999:
		while glob.glob(greater_than_10_output_path + "greater_than_10__00%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	if greater_than_10_last_image > 999 and greater_than_10_last_image <= 9999:
		while glob.glob(greater_than_10_output_path + "greater_than_10__0%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	if greater_than_10_last_image > 9999:
		while glob.glob(greater_than_10_output_path + "greater_than_10__%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	print "\nNext greater_than_10 output image:", greater_than_10_last_image

	if smaller_than_10_last_image <= 9:
		while glob.glob(smaller_than_10_output_path + "smaller_than_10__0000%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	if smaller_than_10_last_image > 9 and smaller_than_10_last_image <= 99:
		while glob.glob(smaller_than_10_output_path + "smaller_than_10__000%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	if smaller_than_10_last_image > 99 and smaller_than_10_last_image <= 999:
		while glob.glob(smaller_than_10_output_path + "smaller_than_10__00%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	if smaller_than_10_last_image > 999 and smaller_than_10_last_image <= 9999:
		while glob.glob(smaller_than_10_output_path + "smaller_than_10__0%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	if smaller_than_10_last_image > 9999:
		while glob.glob(smaller_than_10_output_path + "smaller_than_10__%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	print "Next smaller_than_10 output image:", smaller_than_10_last_image, "\n"




font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (2400,2350)
fontScale              = 5
fontColor              = (255,255,255)
lineType               = 4


def generate_output_image_name(image_class, image_numb):
	if image_numb <= 9:
			image_name = str(image_class) + "__0000" + str(image_numb) + ".jpg"
	if image_numb > 9 and image_numb <= 99:
		image_name = str(image_class) + "__000" + str(image_numb) + ".jpg"
	if image_numb > 99 and image_numb <= 999:
		image_name = str(image_class) + "__00" + str(image_numb) + ".jpg"
	if image_numb > 999 and image_numb <= 9999:
		image_name = str(image_class) + "__0" + str(image_numb) + ".jpg"
	if image_numb > 9999:
		image_name = str(image_class) + "__" + str(image_numb) + ".jpg"

	return image_name


def mouse_crop(event, x, y, flags, param):

	global roi

	# grab references to the global variables
	global x_start, y_start, x_end, y_end, cropping
 
	# if the left mouse button was DOWN, start RECORDING
	# (x, y) coordinates and indicate that cropping is being
	if event == cv2.EVENT_LBUTTONDOWN:
		x_start, y_start, x_end, y_end = x, y, x, y
		cropping = True
 
	# Mouse is Moving
	elif event == cv2.EVENT_MOUSEMOVE:
		if cropping == True:
			#x_end, y_end = x, y
			x_end = x
			y_end = y_start + (x_end - x_start)
 
	# if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates
		#x_end, y_end = x, y
		x_end = x
		y_end = y_start + (x_end - x_start)
		cropping = False # cropping is finished

		#print x_start, y_start, x_end, y_end
		if x_start < x_end and y_start < y_end:
			#print "zzzzzzzzzzz"

 
			refPoint = [(x_start, y_start), (x_end, y_end)]
	 
			if len(refPoint) == 2: #when two points were found
				roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
				cv2.imshow("Cropped", roi)
				#print "aaaaaaaaaaaaaaa"
			clear()
			print colored("Região selecionada com sucesso!", "green")
			print "\nPress:\n\tDOWN to save image in <10cm class\n\tUP to save image in >10cm class\n\tSPACE to get the next image\n\tESC to exit\n"
			print "Press a key...\n"

		else:
			clear()
			print colored("Região selecionada inválida!", "red")
			roi = []
			cv2.destroyWindow("Cropped")
 
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 900, 676)
cv2.setMouseCallback("image", mouse_crop)


#################################
############# START #############
#################################


for img in imglist:

	image = cv2.imread(img)
	oriImage = image.copy()

	clear()
	print "Imagem atual: " + str(img.split("/")[-1])

	verify_dataset()
	print "Selecione uma região da imagem!\n"

	while True:
		i = image.copy()
	 
		if not cropping:
			cv2.imshow("image", image)
	 
		elif cropping:
			cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 3)
			cv2.line(i, (x_start+(x_end-x_start)/2, y_start), (x_start+(x_end-x_start)/2, y_end), (255, 0, 0), 3)

			cv2.line(i, (x_start, y_start+(y_end-y_start)/2), (x_end, y_start+(y_end-y_start)/2), (255, 0, 0), 3)



			#Show size
			size_x = x_end-x_start
			size_y = y_end-y_start
			size = '(' + str(size_x) + ',' + str(size_y) + ')'
			cv2.putText(i, size, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)


			cv2.imshow("image", i)





		# ====================

		# display the image and wait for a keypress

		#Upkey : 82
		#DownKey : 84
		#LeftKey : 81
		#RightKey: 83
		#Space : 32
		#Escape: 27

		key = cv2.waitKey(1) & 0xFF
		#print key

		# if the 'r' key is pressed, reset the cropping region
		#if key == ord("r"):
		#	image = oriImage.copy()

		#DOWN
		if key == 84:
			#print "----------:", roi
			#print type(roi)
			#print len(roi)
			if roi is not "default" and len(roi) > 0:
				output_image_name = generate_output_image_name(smaller_than_10_images_class, smaller_than_10_last_image)
				final_path = smaller_than_10_output_path + output_image_name
				cv2.imwrite(final_path, roi)
				##break
				print colored("Imagem <10cm guardada com sucesso!", "green")
				#index += 1
				verify_dataset()
			else:
				print colored("Imagem não guardada! Selecione uma região!", "red")

		#UP
		if key == 82:
			#print "----------:", roi
			#print type(roi)
			#print len(roi)
			if roi is not "default" and len(roi) > 0:
				output_image_name = generate_output_image_name(greater_than_10_images_class, greater_than_10_last_image)
				final_path = greater_than_10_output_path + output_image_name
				cv2.imwrite(final_path, roi)
				##break
				print colored("Imagem >10cm guardada com sucesso!", "green")
				#index += 1
				verify_dataset()
			else:
				print colored("Imagem não guardada! Selecione uma região!", "red")

		# if the 'SPACE' key is pressed, go to next image
		if key == 32:
			break

		# if the 'c' key is pressed, break from the loop
		#elif key == ord("c"):
		elif key == 27:
			cv2.destroyAllWindows()
			sys.exit()

		# ====================


		cv2.waitKey(1)
 
# close all open windows
cv2.destroyAllWindows()

# Source: https://www.life2coding.com/crop-image-using-mouse-click-movement-python/

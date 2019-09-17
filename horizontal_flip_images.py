#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
from termcolor import colored    # to print colored text in terminal

directory_in = 'dataset/whole_images/greater_than_10/'
directory_out = 'dataset/whole_images/greater_than_10_flipped/'

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


imglist = getListOfFiles(directory_in)

for img_in in imglist:
    # Get image_in path    
    #print img_in

    # Get image_in name
    image_in_name = img_in.split("/")[-1].split(".")[0]
    #print image_in_name

    # Create image_out path
    image_out_path = directory_out + image_in_name + '_flipped' + '.jpg'
    print image_out_path

    # Read image_in
    image_in = cv2.imread(img_in)

    # Flip image_in
    horizontal_flip_image = cv2.flip(image_in, 1)

    # Save horizontal_flip_image
    if cv2.imwrite(image_out_path, horizontal_flip_image):
        print colored("Image flipped successfully!", "green")
    else:
        print colored("Error flipping image!", "red")


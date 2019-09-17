#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random
import sys
import os
from termcolor import colored    # to print colored text in terminal
import shutil

# Defina as percentagens do dataset
train_percentage = 60
validation_percentage = 30
test_percentage = 10

# Defena o número de datasets que pretende criar
dataset_num = 5

total_percentage = train_percentage + validation_percentage + test_percentage

if total_percentage is not 100:
    print "Insira corretamente as percentagens do dataset!"
    sys.exit()

train_percentage = float(train_percentage)/100
validation_percentage = float(validation_percentage)/100
test_percentage = float(test_percentage)/100

#print train_percentage
#print validation_percentage
#print test_percentage

directory_in_greater_than_10 = 'dataset/cropped_images/greater_than_10/'
directory_in_smaller_than_10 = 'dataset/cropped_images/smaller_than_10/'

directory_out = 'dataset/final_datasets/'
directory_out_greater_than_10_train = '/train/greater_than_10/'
directory_out_greater_than_10_validation = '/validation/greater_than_10/'
directory_out_greater_than_10_test = '/test/greater_than_10/'
directory_out_smaller_than_10_train = '/train/smaller_than_10/'
directory_out_smaller_than_10_validation = '/validation/smaller_than_10/'
directory_out_smaller_than_10_test = '/test/smaller_than_10/'

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

def splitFiles(dirImageList, imageType, numDataset):
    #print len(dirImageList)
    #print dirImageList[:10]
    random.shuffle(dirImageList)
    print colored("\nNúmero do dataset: ", "red") + str(numDataset)
    print colored("Tipo de dataset: ", "red") + imageType + "_than_10"
    #print colored("\tTamanho do dataset original:", "green"), len(dirImageList)
    #print dirImageList[:10], "..."

    # Split dirImageList
    # +1 foi para acertar o numero de elementos do dataset de validação porque estava com menos 1 elemento
    dirImageList_splited = np.split(dirImageList, [int(train_percentage * len(dirImageList)), int((train_percentage+validation_percentage) * len(dirImageList))+1])
    #print dirImageList_splited

    # Convert arrays to lists
    train_data = dirImageList_splited[0].tolist()
    validation_data = dirImageList_splited[1].tolist()
    test_data = dirImageList_splited[2].tolist()

    #print colored("\tTamanho do dataset de treino:", "green"), len(train_data)
    #print train_data
    #print colored("\tTamanho do dataset de validação:", "green"), len(validation_data)
    #print validation_data
    #print colored("\tTamanho do dataset de teste:", "green"), len(test_data)
    #print test_data

    final_directory_out_greater_than_10_train = directory_out + "dataset_" + str(numDataset) + directory_out_greater_than_10_train
    #print final_directory_out_greater_than_10_train
    final_directory_out_greater_than_10_validation = directory_out + "dataset_" + str(numDataset) + directory_out_greater_than_10_validation
    #print final_directory_out_greater_than_10_validation
    final_directory_out_greater_than_10_test = directory_out + "dataset_" + str(numDataset) + directory_out_greater_than_10_test
    #print final_directory_out_greater_than_10_test
    final_directory_out_smaller_than_10_train = directory_out + "dataset_" + str(numDataset) + directory_out_smaller_than_10_train
    #print final_directory_out_smaller_than_10_train
    final_directory_out_smaller_than_10_validation = directory_out + "dataset_" + str(numDataset) + directory_out_smaller_than_10_validation
    #print final_directory_out_smaller_than_10_validation
    final_directory_out_smaller_than_10_test = directory_out + "dataset_" + str(numDataset) + directory_out_smaller_than_10_test
    #print final_directory_out_smaller_than_10_test

    # Create all directories
    if imageType is "greater":
        if not os.path.exists(final_directory_out_greater_than_10_train):
            os.makedirs(final_directory_out_greater_than_10_train)
        if not os.path.exists(final_directory_out_greater_than_10_validation):
            os.makedirs(final_directory_out_greater_than_10_validation)
        if not os.path.exists(final_directory_out_greater_than_10_test):
            os.makedirs(final_directory_out_greater_than_10_test)
    if imageType is "smaller":
        if not os.path.exists(final_directory_out_smaller_than_10_train):
            os.makedirs(final_directory_out_smaller_than_10_train)
        if not os.path.exists(final_directory_out_smaller_than_10_validation):
            os.makedirs(final_directory_out_smaller_than_10_validation)
        if not os.path.exists(final_directory_out_smaller_than_10_test):
            os.makedirs(final_directory_out_smaller_than_10_test)

    # Copy images
    if imageType is "greater":
        for img_in in train_data:
            shutil.copy(img_in, final_directory_out_greater_than_10_train)
        for img_in in validation_data:
            shutil.copy(img_in, final_directory_out_greater_than_10_validation)
        for img_in in test_data:
            shutil.copy(img_in, final_directory_out_greater_than_10_test)

    if imageType is "smaller":
        for img_in in train_data:
            shutil.copy(img_in, final_directory_out_smaller_than_10_train)
        for img_in in validation_data:
            shutil.copy(img_in, final_directory_out_smaller_than_10_validation)
        for img_in in test_data:
            shutil.copy(img_in, final_directory_out_smaller_than_10_test)

# Criar o dataset greater_than_10
for x in range(dataset_num):
    imglist = getListOfFiles(directory_in_greater_than_10)
    splitFiles(imglist, "greater", x+1)

# Criar o dataset smaller_than_10
for x in range(dataset_num):
    imglist = getListOfFiles(directory_in_smaller_than_10)
    splitFiles(imglist, "smaller", x+1)

# K-fold coross-validadion: https://stats.stackexchange.com/questions/223408/how-does-k-fold-cross-validation-fit-in-the-context-of-training-validation-testi


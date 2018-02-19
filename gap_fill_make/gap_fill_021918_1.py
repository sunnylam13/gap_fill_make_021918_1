# -*- coding: utf-8 -*-

# ! /usr/local/Cellar/python3/3.6.1

# File Name Numbering Gap Filler - This program finds all files with a given prefix in a single folder and locates any gaps in numbering (i.e. spam001.txt, spam003.txt, missing spam002.txt)...

# USAGE
# xxxx

import os, re, shutil
import fileFunc021918v1 as fileTools

# testing
# print(fileTools.abs_cwd_file_path)

#####################################
# USER INPUT
#####################################

# user_input_folder = input("Please enter the path to the folder you want to fill the gaps in.  We suggest this be in the form of a string:  ")

# testing
user_input_folder = "../docs/testFolder1" # assign the folder to the input variable so I don't have to run the code over and over

#####################################
# END USER INPUT
#####################################

#####################################
# REGEX
#####################################

# prefix_regex1 = re.compile(r'(^[a-z]+)')

prefix_regex2 = re.compile(r'''
		(^[a-z]+) # this is the gropu for the prefix, assumed to be a-z letters, one or more
		(0*) # this is the the group for leading zeros, 0 or more i.e. 00 of 001
		([1-9]*) # this is the group for the numbering
	''', re.VERBOSE)

## Testing

# mo_a1 = prefix_regex2.search("spam001.txt")
# print(mo_a1)
# # test groupings
# print(mo_a1.group(1))
# print(mo_a1.group(2))
# print(mo_a1.group(3))


# get the absolute file path of the current working directory of program
abs_cwd_path = fileTools.abs_cwd_file_path # set the destination file path to be the current working directory or cwd

# a list of all folders and subfolders to be analyzed
folder_path_list = [] # a list to hold all finalized folder paths (not folder names)

# a list of all files to be analyzed
file_path_list = [] # a list to hold all finalized folder paths (not folder names)


#####################################
# END REGEX
#####################################

def analyze_files(foldername,folder_path_list,file_path_list):
	fileTools.scanFolder(foldername,folder_path_list)
	fileTools.scanFile(foldername,file_path_list)

	print(folder_path_list) # for testing
	print(file_path_list) # for testing

def gap_fill(foldername):
	# figure out what the given prefix is using regex and the groups for substitution
	# analyze the number of said files and determine what the gap is
	# fix the gap by renaming the later files so that the gap is closed
	pass

#####################################
# EXECUTION
#####################################

analyze_files(user_input_folder,folder_path_list,file_path_list)

#####################################
# END EXECUTION
#####################################


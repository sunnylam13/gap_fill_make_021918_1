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
		(^[a-z]+) # this is the group for the prefix, assumed to be a-z letters, one or more
		(0*) # this is the the group for leading zeros, 0 or more i.e. 00 of 001
		([1-9]*) # this is the group for the numbering
	''', re.VERBOSE)

## Testing

# mo_a1 = prefix_regex2.search("spam001.txt")
# print(mo_a1)
# # test groupings
# print(mo_a1.group(1)) # spam
# print(mo_a1.group(2)) # 00
# print(mo_a1.group(3)) # 1

# # this regex version handles file paths rather than file names
# # https://regexr.com/3l1go
# prefix_regex3 = re.compile(r'''
# 		(^.*) # this is the group for the beginning of the filename until the leading zeroes if any
# 		(0+) # captures the leading zeroes if any
# 		([1-9]*) # this is the numbering we want to analyze
# 		(\.) # this is the dot before the extension
# 		(.*$) # this is the extension after the dot
# 	''', re.VERBOSE)

# mo_a2 = prefix_regex2.search("../docs/testFolder1/spam003.txt")
# print(mo_a2)
# # test groupings
# print(mo_a2.group(1))
# print(mo_a2.group(2))
# print(mo_a2.group(3))
# print(mo_a2.group(4))
# print(mo_a2.group(5))

#####################################
# END REGEX
#####################################

#####################################
# VARIABLES
#####################################

# get the absolute file path of the current working directory of program
abs_cwd_path = fileTools.abs_cwd_file_path # set the destination file path to be the current working directory or cwd

# # a list of all folders and subfolders to be analyzed
# folder_path_list = [] # a list to hold all finalized folder paths (not folder names)

# list of filenames that can be indexed to the correct file path list
filename_list_f = []

# a list of all files to be analyzed
file_path_list = [] # a list to hold all finalized folder paths (not folder names)

# a dict to store filenames and their corresponding file path
file_dict_master = {}

#####################################
# END VARIABLES
#####################################

def store_file_dict(filename,filename_list,file_dict_master):
	# store the filename and its path in file_dict_master dictionary
	
	filename_index = filename_list.index(filename) # get the index number of file in filename_list
	filename_path_value = file_path_list[filename_index] # get the value or filename path at the same index position as filename_index
	file_dict_master[filename] = filename_path_value # if it matches, store it in a dict with the filename as the key and its filepath as the value

def check_numbering(filename_list,file_path_list,regex,file_dict_master):
	# check files and locate numbering gaps
	current_num = 1
	for file in filename_list:
		analyze_filename = regex.search(file)
		# current_num = filename_list.index(file) + 1 # can't tie it to current index of file, it could be wrong, tie it to a separate counter
		if int(analyze_filename.group(3)) == (current_num):
			# if the number of the filename matches the index number of its position + 1 (since index starts at 0 and we want to match 1 with 1 for example)
			
			# store the filename and its path in file_dict_master dictionary
			store_file_dict(file,filename_list,file_dict_master)

			current_num += 1 # increment counter
		else:
			# otherwise if it doesn't match at all
			# set the number to match the current index number
			fix_numbering(filename_list,file_path_list,regex,file_dict_master)

def analyze_files(foldername,filename_list,file_path_list,file_dict_master):
	# generate list of file names and corresponding list of paths to each of those file names that will be altered
	filename_list = fileTools.scanFile(foldername,file_path_list)

	# for testing
	print("The file name list is:  ")
	# print(filename_list)
	for filename in filename_list:
		print(filename)
	print("The file name path list is:  ")
	# print(file_path_list)
	for filename in file_path_list:
		print(filename)
	

	check_numbering(filename_list,file_path_list,prefix_regex2,file_dict_master)

def fix_numbering(filename_list,file_path_list,regex,file_dict_master):
	# rename all later files after a gap is discovered so numbering is in sync
	# change the filename using regex substitution
	# then find its corresponding position on the file_path_list
	# use the new filename after substitution to do another regex sub to change its name entry in its file path in the file_path_list 
	pass

#####################################
# EXECUTION
#####################################

# analyze_files(user_input_folder,folder_path_list,file_path_list)
analyze_files(user_input_folder,filename_list_f,file_path_list,file_dict_master)

#####################################
# END EXECUTION
#####################################


# -*- coding: utf-8 -*-

# ! /usr/local/Cellar/python3/3.6.1

# File Name Numbering Gap Maker - This program inserts gaps into numbered files so that a new file can be added.

# USAGE
# python3 gap_make_021918_1.py

import os, re, shutil
import fileFunc021918v1 as fileTools
# import gap_fill_021918_1 as gapFiller

#####################################
# VARIABLES GENERAL
#####################################

# Get the user input folder with list of numbered files.
# user_input_folder = input("Please enter the file path to the folder with the numbered files you wish to create the gap for.")

# testing
user_input_folder = "../docs/testFolder2" # assign the folder to the input variable so I don't have to run the code over and over
# there are 87 files
# docs/testFolder2/spam001.txt
# docs/testFolder2/spam002.txt
# docs/testFolder2/spam003.txt
# docs/testFolder2/spam004.txt
# docs/testFolder2/spam005.txt
# docs/testFolder2/spam006.txt
# docs/testFolder2/spam007.txt

# Get the number of files in the folder.
true_max_num = len(os.listdir(user_input_folder)) # actual upper limit of numbering unlike highest_labelled_number()
# print("The true_max_num is:  %i\n" % true_max_num)

# Get the user input on where they want to insert the gap.

# user_number_pos_input = input("""
# 		Please tell the program at which number you wish to insert the gap before or after.\n
# 		The command should be along the lines of...\n
# 		after 2\n
# 		before 1\n
# 		after 5\n
# 		before 3\n
# 		As examples of the command you should use...\n
# 	""")

# testing
user_number_pos_input = "before 1" # assign this so you don't have to enter a user prompt
# user_number_pos_input = "after 5"

abs_cwd_path = fileTools.abs_cwd_file_path # set the destination file path to be the current working directory or cwd

# list of the original filenames that can be indexed to the correct file path list
filename_list = []

# a list of all original file paths to be analyzed
file_path_list = [] # a list to hold all finalized folder paths (not folder names)

# processing file name list
proc_file_list = []

# processing file name path list
proc_filePath_list = []

# the final list of file names
file_list_final = []

# the final list of all new file paths (what the final copying should be)
filePath_list_final = []

#####################################
# END VARIABLES GENERAL
#####################################


#####################################
# REGEX
#####################################

# find out whether the user commanded "before/after" "#" using regex

# https://regexr.com/3l8tl
user_cmnd_before_regex1 = re.compile(r'''
		(?P<command>before) # this is the before command given by user
		(?P<space>\s) # this is the space between command and the file number user wants to insert before
		(?P<number>\d+) # this is the file number
	''', re.VERBOSE)

# https://regexr.com/3l8tu
user_cmnd_after_regex1 = re.compile(r'''
		(?P<command>after) # this is the after command given by user
		(?P<space>\s) # this is the space between command and the file number user wants to insert before
		(?P<number>\d+) # this is the file number
	''', re.VERBOSE)

# you need to analyze the file name itself to find its label number

# prefix_and_number_1 = gapFiller.prefix_regex2 # get it from imported file

prefix_regex2 = re.compile(r'''
		(?P<prefixLetters>^[a-z]+) # this is the group for the prefix, assumed to be a-z letters, one or more
		(?P<leadZeroes>0*) # this is the the group for leading zeros, 0 or more i.e. 00 of 001
		(?P<numbering>[1-9]*) # this is the group for the numbering
		(?P<extension>(\..*$)) # this is the extension
	''', re.VERBOSE)

#####################################
# END REGEX
#####################################


#####################################
# FUNCTIONS/METHODS
#####################################


def analyze_files(user_input_folder,filename_list,file_path_list):
	# generate list of file names and corresponding list of paths to each of those file names that will be altered
	filename_list = fileTools.scanFile(user_input_folder,file_path_list)

	# create the processing files
	# proc_file_list
	# proc_filePath_list
	
	# create the processing files at last
	for filename in filename_list:
		# print("Current file being analyzed is:  %s" % filename) # testing
		file_current_index = filename_list.index(filename)
		process_file_lists(filename,filename_list,file_path_list,file_current_index)

	# we need to fix the processing files order
	# because sometimes spam003.txt starts off the list for some reason rather than spam001.txt which screws things up a bit
	proc_file_list.sort()
	proc_filePath_list.sort()

	# # start fixing the numbering
	# fix_numbering(proc_file_list,proc_filePath_list,regex)

def process_file_lists(filename,filename_list,file_path_list,file_current_index):
	proc_file_list.append(filename) # append the file name into the proc_file_list
	proc_filePath_list.append(file_path_list[file_current_index]) # append the file path corresponding to the same index position as filename in filename_list

#####################################
# END FUNCTIONS/METHODS
#####################################



#####################################
# EXECUTION
#####################################

# Scan the user input folder for a list of numbered files.  Store all the file names in a new list.
analyze_files(user_input_folder,filename_list,file_path_list)
# testing
print("proc_file_list is:  ")
print(proc_file_list)
print("proc_filePath_list is:  ")
print(proc_filePath_list)

#####################################
# END EXECUTION
#####################################





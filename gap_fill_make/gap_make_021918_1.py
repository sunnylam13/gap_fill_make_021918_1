# -*- coding: utf-8 -*-

# ! /usr/local/Cellar/python3/3.6.1

# File Name Numbering Gap Maker - This program inserts gaps into numbered files so that a new file can be added.

# USAGE
# xxxx

import os, re, shutil

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

#####################################
# END REGEX
#####################################


#####################################
# FUNCTIONS/METHODS
#####################################

def user_input_analyze():
	pass

#####################################
# END FUNCTIONS/METHODS
#####################################



#####################################
# EXECUTION
#####################################



#####################################
# END EXECUTION
#####################################





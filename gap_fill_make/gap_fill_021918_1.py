# -*- coding: utf-8 -*-

# ! /usr/local/Cellar/python3/3.6.1

# File Name Numbering Gap Filler - This program finds all files with a given prefix in a single folder and locates any gaps in numbering (i.e. spam001.txt, spam003.txt, missing spam002.txt)...

# USAGE
# xxxx

import os, re, shutil

#####################################
# USER INPUT
#####################################

user_input_folder = input("Please enter the path to the folder you want to fill the gaps in.  We suggest this be in the form of a string:  ")

#####################################
# END USER INPUT
#####################################

#####################################
# REGEX
#####################################

prefix_regex1 = re.compile(r'(^[a-z]+)')

prefix_regex2 = re.compile(r'''
		(^[a-z]+) # this is the gropu for the prefix, assumed to be a-z letters, one or more
		(0*) # this is the the group for leading zeros, 0 or more i.e. 00 of 001
		([1-9]*) # this is the group for the numbering
	''', re.VERBOSE)

#####################################
# END REGEX
#####################################

def gap_fill(foldername):
	# figure out what the given prefix is using regex and the groups for substitution
	# analyze the number of said files and determine what the gap is
	# fix the gap by renaming the later files so that the gap is closed


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

# get the base path of the folder
input_folder_dir = os.path.basename(user_input_folder)
# print("The base name path to the folder is:  %s" % input_folder_dir)

input_folder_filename_list = os.listdir(user_input_folder)

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
# assign this so you don't have to enter a user prompt
# user_number_pos_input = "before 1" 
user_number_pos_input = "after 5"

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

shadow_filename_list = [] # you will analyze this list to find the names with "-clone"
shadow_filepath_list = [] # you will use the modifications based on clone_filename_list to generate non "-clone" links

#####################################
# END VARIABLES GENERAL
#####################################


#####################################
# REGEX
#####################################

# find out whether the user commanded "before/after" "#" using regex

# # https://regexr.com/3l8tl
# user_cmnd_before_regex1 = re.compile(r'''
# 		(?P<command>before) # this is the before command given by user
# 		(?P<space>\s) # this is the space between command and the file number user wants to insert before
# 		(?P<number>\d+) # this is the file number
# 	''', re.VERBOSE)

# # https://regexr.com/3l8tu
# user_cmnd_after_regex1 = re.compile(r'''
# 		(?P<command>after) # this is the after command given by user
# 		(?P<space>\s) # this is the space between command and the file number user wants to insert before
# 		(?P<number>\d+) # this is the file number
# 	''', re.VERBOSE)

# https://regexr.com/3l911
# after|before
user_cmnd_any_regex1 = re.compile(r'''
		(?P<command>after|before) # this is the command given by user
		(?P<space>\s) # this is the space between command and the file number user wants to insert before
		(?P<number>\d+) # this is the file number
	''', re.VERBOSE)


# you need to analyze the file name itself to find its label number

# prefix_and_number_1 = gapFiller.prefix_regex2 # get it from imported file

prefix_regex2 = re.compile(r'''
		(?P<prefixLetters>^[a-z]+) # this is the group for the prefix, assumed to be a-z letters, one or more
		(?P<leadZeroes>0*) # this is the the group for leading zeros, 0 or more i.e. 00 of 001
		(?P<numbering>[1-90]*) # this is the group for the numbering
		(?P<extension>(\..*$)) # this is the extension
	''', re.VERBOSE)


# need regex search that finds files you've now renamed "xxxx.ext-clone"
# assumes you're working with ../docs/testFolder2/spam007.txt-clone
clone_regex1 = re.compile(r'''
		(?P<prefixLetters>^[a-z]+) # this is the group for the prefix, assumed to be a-z letters, one or more
		(?P<leadZeroes>0*) # this is the the group for leading zeros, 0 or more i.e. 00 of 001
		(?P<numbering>[1-90]*) # this is the group for the numbering
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
		# Create file paths for the original list of numbered files.  Store all the file paths in the original file path list.
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

def analyze_command(regex):
	regex_result = user_cmnd_any_regex1.search(user_number_pos_input) # use regex to analyze the user's input and find the commands and the file number
	user_selected_cmd = regex_result.group('command')
	user_selected_num = int(regex_result.group('number')) # store the user selected number and convert to integer

	return (regex_result,user_selected_cmd,user_selected_num)

def create_gap(proc_file_list,proc_filePath_list):
	# Go to the index position of the number user entered.
	# regex_result = user_cmnd_any_regex1.search(user_number_pos_input) # use regex to analyze the user's input and find the commands and the file number
	# user_selected_cmd = regex_result.group('command')
	# user_selected_num = int(regex_result.group('number')) # store the user selected number and convert to integer

	regex_result,user_selected_cmd,user_selected_num = analyze_command(user_number_pos_input)
	# print(regex_result)
	# print(user_selected_cmd)
	# print(user_selected_num)

	convert_user_num_to_index_pos = user_selected_num - 1 # since index positions start at 0 and not 1, to find that numbered file's index position subtract 1... NOTE:  this assumes that there are no other gaps in numbering that are there or that don't matter, if not, you may way to run the gap filler program first and then run this program
	
	if user_selected_cmd == "before":
		# If they used "insert before", change the original file name at the position and every file after by increasing it's label number by +1.  Append/store the change in the new file name list.
		try:
			# add all of the files before the user selected file that remain unchanged
			for x in range(0,convert_user_num_to_index_pos):
				# append that altered_fileName to file_list_final
				file_list_final.append(proc_file_list[x])
				print("The unchanged filename is:  %s\n" % proc_file_list[x])

				# add a copy to the shadow file list
				# this solves the index out of range error later on with strip_copy_tag()
				shadow_filename_list.append(proc_file_list[x])

			# Go to the index position of the number user entered.
			# start a loop here that changes current index position file name and all file names after by 1
			for x in range(convert_user_num_to_index_pos,len(proc_file_list)): # loop from user chosen file name to the end of the list
				# testing
				print("The file analyzed is:  %s" % proc_file_list[x])
				
				# get the name of the file at x and create a regex object to use for constructing new name
				
				regex_filename_analysis = prefix_regex2.search(proc_file_list[x])
				# use regex substitution of sorts to create new name
				# print("The regex is:  ")
				# print(regex_filename_analysis)
				# print(regex_filename_analysis.group('prefixLetters'))
				# print(regex_filename_analysis.group('leadZeroes'))
				# print(str(convert_user_num_to_index_pos + 1))
				# print(regex_filename_analysis.group('extension'))

				# use (x+2) because (x + 1) would only give us back the current file index
				altered_fileName = regex_filename_analysis.group('prefixLetters') + regex_filename_analysis.group('leadZeroes') + str(x + 2) + regex_filename_analysis.group('extension') + "_copy" # the temporary file name to use to avoid error
				shadow_altered_fileName = regex_filename_analysis.group('prefixLetters') + regex_filename_analysis.group('leadZeroes') + str(x + 2) + regex_filename_analysis.group('extension') # the file name as it should be, for the final naming phase
				
				# append that altered_fileName to file_list_final
				file_list_final.append(altered_fileName)
				print("The altered_fileName is:  %s\n" % altered_fileName)

				shadow_filename_list.append(shadow_altered_fileName)

		except Exception as e:
			print("There is an error in creating a gap before file number %i" % user_selected_num)
			print("The error is:  ")
			print(e)
		else:
			pass
	elif user_selected_cmd == "after":
		# If they used "insert after", don't change the original file name at the position.  Instead change every file after by increasing its label number by +1. Append/store the change in the new file name list.
		try:
			# add all of the files before the user selected file that remain unchanged
			for x in range(0,convert_user_num_to_index_pos + 1):
				# append that altered_fileName to file_list_final
				file_list_final.append(proc_file_list[x])
				print("The unchanged filename is:  %s\n" % proc_file_list[x])

				# add a copy to the shadow file list
				# this solves the index out of range error later on with strip_copy_tag()
				shadow_filename_list.append(proc_file_list[x])

			for x in range(convert_user_num_to_index_pos + 1,len(proc_file_list)): # loop from user chosen file name to the end of the list
				# testing
				print("The file analyzed is:  %s" % proc_file_list[x])
				
				# get the name of the file at x and create a regex object to use for constructing new name
				
				regex_filename_analysis = prefix_regex2.search(proc_file_list[x])
				# use regex substitution of sorts to create new name
				# print("The regex is:  ")
				# print(regex_filename_analysis)
				# print(regex_filename_analysis.group('prefixLetters'))
				# print(regex_filename_analysis.group('leadZeroes'))
				# print(str(convert_user_num_to_index_pos + 1))
				# print(regex_filename_analysis.group('extension'))

				altered_fileName = regex_filename_analysis.group('prefixLetters') + regex_filename_analysis.group('leadZeroes') + str(x + 2) + regex_filename_analysis.group('extension') + "_copy" # the temporary file name to use to avoid error
				shadow_altered_fileName = regex_filename_analysis.group('prefixLetters') + regex_filename_analysis.group('leadZeroes') + str(x + 2) + regex_filename_analysis.group('extension') # the file name as it should be, for the final naming phase
				
				# append that altered_fileName to file_list_final
				file_list_final.append(altered_fileName)
				print("The altered_fileName is:  %s\n" % altered_fileName)

				shadow_filename_list.append(shadow_altered_fileName)
		except Exception as e:
			print("There is an error in creating a gap after file number %i" % user_selected_num)
			print("The error is:  ")
			print(e)
		else:
			pass

	# for each filename in file_list_final, construct filePath_list_final
	
	for filename in file_list_final:
		# rel_path = os.path.join(input_folder_dir,filename)
		# rel_path = os.path.join(user_input_folder,filename) # easier
		# abs_path = filePath_list_final.append(os.path.abspath(rel_path))

		filePath_list_final.append(os.path.join(user_input_folder,filename)) # even easier, since user should have already provided full absolute path for a folder outside of the current working directory

	for filename in shadow_filename_list:
		shadow_filepath_list.append(os.path.join(user_input_folder,filename)) # even easier, since user should have already provided full absolute path for a folder outside of the current working directory


def strip_copy_tag(filePath_list_final):

	# testing
	# print("filePath_list_final is")
	# print(filePath_list_final)
	# print("shadow_filepath_list")
	# print(shadow_filepath_list)

	try:
		for filepath in filePath_list_final:
			file_current_index = filePath_list_final.index(filepath)
			if filepath == shadow_filepath_list[file_current_index]:
				pass # continue on if the paths are the same
			elif filepath is not shadow_filepath_list[file_current_index]:
				# if they are not the same
				rename_single_filePath(filepath,shadow_filepath_list[file_current_index])
	except Exception as e:
		print("You have an error in strip_copy_tag function.")
		print(e)
		print("\n\n")
	else:
		pass


def rename_single_filePath(old_filepath,new_file_path):
	# this function takes a passed string of a file path not a filename
	# since it uses shutil.move(old_path,new_path)
	try:
			if old_filepath == new_file_path:
				pass
			else:
				shutil.move(old_filepath,new_file_path)
	except Exception as e:
		print("There is an error in rename_single_filePath function.  The error is:  ")
		print(e)
		print("\n\n")
	else:
		pass

def rename_files(old_file_path_list,new_file_path_list):
	# use shutil.move to rename the file
	# shutil.move(old_path,new_path)
	# this works with an entire list of file paths and is not suitable for fixing individual files

	try:
		for item in old_file_path_list:
		# item is the old file path
			get_item_index = old_file_path_list.index(item)
			
			if item == new_file_path_list[get_item_index]:
				print("The old file path was not replaced:  %s" % (item))
				pass
			else:
				print("The old file path replaced:  %s" % (item))
				print("The new file path is:  %s" % (new_file_path_list[get_item_index]))
				shutil.move(item,new_file_path_list[get_item_index])
	except Exception as e:
		print("There is an error in rename_files function.  The error is:  ")
		print(e)
		print("\n\n")
	else:
		pass

#####################################
# END FUNCTIONS/METHODS
#####################################



#####################################
# EXECUTION
#####################################

# Scan the user input folder for a list of numbered files.  Store all the file names in a new list.
analyze_files(user_input_folder,filename_list,file_path_list)
# testing
# print("proc_file_list is:  ")
# print(proc_file_list)
# print("proc_filePath_list is:  ")
# print(proc_filePath_list)

create_gap(proc_file_list,proc_filePath_list)
# testing
# print("file_list_final is:  ")
# print(file_list_final)
# print("filePath_list_final is:  ")
# print(filePath_list_final)

# original and new file names and paths have been generated
# all that remains is to execute the change
rename_files(proc_filePath_list,filePath_list_final)

# strip the "_copy" tags
strip_copy_tag(filePath_list_final)

#####################################
# END EXECUTION
#####################################





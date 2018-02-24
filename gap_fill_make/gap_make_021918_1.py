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
		(?P<numbering>[1-9]*) # this is the group for the numbering
		(?P<extension>(\..*$)) # this is the extension
	''', re.VERBOSE)


# need regex search that finds files you've now renamed "xxxx.ext-clone"
# assumes you're working with ../docs/testFolder2/spam007.txt
clone_regex1 = re.compile(r'''
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
				altered_fileName = regex_filename_analysis.group('prefixLetters') + regex_filename_analysis.group('leadZeroes') + str(x + 2) + regex_filename_analysis.group('extension')
				
				# append that altered_fileName to file_list_final
				file_list_final.append(altered_fileName)
				print("The altered_fileName is:  %s\n" % altered_fileName)

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

				# use (x+2) because (x + 1) would only give us back the current file index
				altered_fileName = regex_filename_analysis.group('prefixLetters') + regex_filename_analysis.group('leadZeroes') + str(x + 2) + regex_filename_analysis.group('extension')
				
				# append that altered_fileName to file_list_final
				file_list_final.append(altered_fileName)
				print("The altered_fileName is:  %s\n" % altered_fileName)
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

def fix_numbering(proc_file_list,proc_filePath_list,regex):
	# rename all later files after a gap is discovered so numbering is in sync
	# change the filename using regex substitution
	# then find its corresponding position on the file_path_list
	# use the new filename after substitution to do another regex sub to change its name entry in its file path in the file_path_list 
	


	for filename in proc_file_list:
		print("Filename to be analyzed is:  %s" % (filename))
		# analyze_filename = regex.search(filename)
		# current_filename_index = proc_file_list.index(filename)
		
		setup_src_dst_paths(filename,proc_file_list,proc_filePath_list,regex) # should assign it in the order of the returned values from the function

	# testing
	# print("The proc_file_list is:\n")
	# print(proc_file_list) # testing
	# print("The length of proc_file_list is:  %i" % len(proc_file_list))
	# print("\n")
	# print("The proc_filePath_list is:\n")
	# print(proc_filePath_list) # testing
	# print("The length of proc_filePath_list is:  %i" % len(proc_filePath_list))
	# print("\n")
	# print("The file_list_final is:\n")
	# print(file_list_final) # testing
	# print("The length of file_list_final is:  %i" % len(file_list_final))
	# print("\n")
	# print("The filePath_list_final is:\n")
	# print(filePath_list_final) # testing
	# print("The length of filePath_list_final is:  %i" % len(filePath_list_final))
	# print("\n")

def setup_src_dst_paths(filename,proc_file_list,proc_filePath_list,regex):
	regex_result = regex.search(filename) # aka. regex_result
	current_filename_index = proc_file_list.index(filename)
	# print("The current filename index position is:  %i" % current_filename_index)
	file_old_num = int(regex_result.group('numbering'))
	# print("The file's original label number is:  %i" % file_old_num)
	print("We want to change the label number %i to the new number %i" % (file_old_num,current_filename_index+1))

	# print("The highest label number in the set is:  %i" % highest_label_num)

	# find the file with number 1
	# if you can't find it then, cycle through proc_file_list until you do
	# if you find it add it to the file_list_final,filePath_list_final
	# if you still can't find it, grab the file in the index + 1 position or the next file on the list and change it to be 1
	# rinse and repeat

	try:
		
		# where we want to start our search with 1 (meaning x + 1)
		target_num = current_filename_index + 1

		if file_old_num == target_num: # if the file's number matches the number it should be
			file_list_final.append(filename)
			filePath_list_final.append(proc_filePath_list[current_filename_index])
			print("\n")
			# print(file_list_final)
			# print(filePath_list_final)
		elif (file_old_num is not target_num) and (file_old_num is not highest_label_num):  # if the file's number does not match the number and is not the last number
			# if you still can't find it, grab the file in the index + y position or the next file on the list and change it to be y
			# print("(file_old_num is not target_num) and (file_old_num is not highest_label_num) works")
			fileNum_changer(filename,current_filename_index,proc_file_list,regex,file_old_num)
		else:
			pass

		if file_old_num == highest_label_num:
			# use len(proc_file_list) to get the last number that the last file should have not true_max_num...
			print("`file_old_num == highest_label_num` works")
			fileNum_changer(filename,current_filename_index,proc_file_list,regex,file_old_num,true_max_num) # can't use current_filename_index + 1 here or it goes out of range, can do it within fileNum_changer
	except Exception as e:
		print("There's an error in your setup_src_dst_paths function:  ")
		print(e)
		print("\n\n")
	else:
		pass

def fileNum_changer(filename,current_filename_index,proc_file_list,regex,file_old_num,max_num=0):
	# helper function for setup_src_dst_paths()
	
	print("The current_filename_index is: %i" % current_filename_index)

	if max_num > 0:
		# if new_num argument is passed skip this logic code
		# print(new_num)
		new_num = max_num
		print("If this is the last file, new_num index is:  %i" % new_num)
	else:
		# otherwise give new_num a value
		new_num = current_filename_index+1
		print("The non-last file new_num target number is %i" % new_num)
	

	try:

		# change the filename's file_old_num to the new_number
		# store it in altered_fileName

		regex_result = regex.search(filename) # aka. regex_result
		# change that target_fileName to the new number (new_num) creating altered_fileName
		altered_fileName = regex_result.group('prefixLetters') + regex_result.group('leadZeroes') + str(new_num) + regex_result.group('extension')
		# append that altered_fileName to file_list_final
		file_list_final.append(altered_fileName)
		print("The altered_fileName is:  %s\n" % altered_fileName)

		# create a new path for that altered_fileName in filePath_list_final
		
		old_path = proc_filePath_list[current_filename_index]
		# print("The old path is:  %s" % (old_path)) # testing
		
		# get the dir path to the original filename from proc_filePath_list
		dirPath = os.path.dirname(old_path)
		# print("The directory path is:  %s" % (dirPath)) # testing

		# using the altered_fileName and dirPath, create a new path target for re-naming
		new_path = os.path.join(dirPath,altered_fileName)
		# print("The new path is:  %s" % (new_path)) # testing

		# push the new file path into the filePath_list_final
		filePath_list_final.append(new_path)
	except Exception as e:
		print("There is an error in fileNum_changer function:  ")
		print(e)
		print("\n\n")
	else:
		pass

def rename_files(old_filenames,new_filenames,old_file_path,new_file_path):
	# old_file_path and new_file_path are lists of paths not a single path
	# use shutil.move to rename the file
	# shutil.move(old_path,new_path)

	regex_result,user_selected_cmd,user_selected_num = analyze_command(user_number_pos_input)
	clone_filename_list = []
	clone_path_list = []

	try:
		for item in old_file_path:
		# item is the old file path
			get_item_index = old_file_path.index(item)
			

			if user_selected_cmd == "after":

				if item == new_file_path[get_item_index]:
					print("The old file path was not replaced:  %s" % (item))
					clone_filename_list.append(new_filenames[get_item_index] + "-clone")
					clone_path_list.append(new_file_path[get_item_index] + "-clone")
					print("The file clone name is:  %s\n" % (new_filenames[get_item_index] + "-clone"))
					print("The file clone_path is:  %s\n" % (new_file_path[get_item_index] + "-clone"))
					pass
				elif (item is not new_file_path[get_item_index]) and (get_item_index is not len(old_file_path)): # if the current file is not in the list of newly minted file paths and is not the last file to be processed
					# print("The old file path replaced:  %s" % (item))
					# print("The new file path is:  %s" % (new_file_path[get_item_index]))

					# # the filename ahead already exists, the one before being renamed to match it overwrites leaving you with a gap
					# # store original filename
					# # create a copy of said original file path
					# prep_copy_for_rename = old_file_path[get_item_index + 1]

					# # shutil.move(item,new_file_path[get_item_index])

					# # place the copy back



					# the filename ahead already exists, the one before being renamed to match it overwrites leaving you with a gap
					# create a copy of said original file name and file path
					clone_filename_list.append(new_filenames[get_item_index + 1] + "-clone")
					clone_path_list.append(new_file_path[get_item_index + 1] + "-clone")
					print("The file clone name is:  %s\n" % (new_filenames[get_item_index + 1] + "-clone"))
					print("The file clone_path is:  %s\n" % ((new_file_path[get_item_index + 1] + "-clone")) )

					# now rename the file to the number that's one ahead i.e. 006 becomes 007-copy
					# shutil.move(item,new_file_path[get_item_index])
					# shutil.move(clone_path,new_file_path[get_item_index])

					# this means that by this point all the files you've now renamed are "xxxx.ext-clone"
					# now you want to remove the "-clone" part
					
					# get the list of files in the folder, create another list of file paths to cycle through
					new_fileName_list, new_filePath_list = []
					new_filePath_list = fileTools.scanFile(user_input_folder,new_fileName_list) # since the function returns new_fileName_list

					for item in new_fileName_list:
						pass

					print("The old file path replaced:  %s" % (item))
					print("The new file path is:  %s" % (new_file_path[get_item_index]))

				elif (get_item_index == len(old_file_path)): # if the current file is the last file
					pass
			elif user_selected_cmd == "before":
				pass
			else:
				print("Error - user did not provide a command!")

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
print("proc_file_list is:  ")
print(proc_file_list)
print("proc_filePath_list is:  ")
print(proc_filePath_list)

create_gap(proc_file_list,proc_filePath_list)
# testing
print("file_list_final is:  ")
print(file_list_final)
print("filePath_list_final is:  ")
print(filePath_list_final)

# original and new file names and paths have been generated
	# all that remains is to execute the change
rename_files(proc_file_list,file_list_final,proc_filePath_list,filePath_list_final)

#####################################
# END EXECUTION
#####################################





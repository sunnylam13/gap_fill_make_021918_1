# -*- coding: utf-8 -*-

# ! /usr/local/Cellar/python3/3.6.1

# File Name Numbering Gap Filler - This program finds all files with a given prefix in a single folder and locates any gaps in numbering (i.e. spam001.txt, spam003.txt, missing spam002.txt)...

# USAGE
# python3 gap_fill_021918_1.py

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

# (^[a-z]+)(0*)([1-9]*)(\..*$)
prefix_regex2 = re.compile(r'''
		(?P<prefixLetters>^[a-z]+) # this is the group for the prefix, assumed to be a-z letters, one or more
		(?P<leadZeroes>0*) # this is the the group for leading zeros, 0 or more i.e. 00 of 001
		(?P<numbering>[1-90]*) # this is the group for the numbering
		(?P<extension>(\..*$)) # this is the extension
	''', re.VERBOSE)

## Testing

# mo_a1 = prefix_regex2.search("spam001.txt")
# print(mo_a1)
# # test groupings
# print(mo_a1.group(1)) # spam
# print(mo_a1.group(2)) # 00
# print(mo_a1.group(3)) # 1

#####################################
# END REGEX
#####################################

#####################################
# VARIABLES
#####################################

# get the absolute file path of the current working directory of program
abs_cwd_path = fileTools.abs_cwd_file_path # set the destination file path to be the current working directory or cwd

# list of filenames that can be indexed to the correct file path list
filename_list = []

# a list of all files to be analyzed
file_path_list = [] # a list to hold all finalized folder paths (not folder names)

# processing file name list
proc_file_list = []

# processing file name path list
proc_filePath_list = []

# we need the number of files in the use input directory so we know what the final number to use is

true_max_num = len(os.listdir(user_input_folder)) # actual upper limit of numbering unlike highest_labelled_number()
# print("The true_max_num is:  %i\n" % true_max_num)

file_list_final = []

filePath_list_final = []

#####################################
# END VARIABLES
#####################################

def highest_labelled_number (user_input_folder,regex):
	dirs = os.listdir(user_input_folder) # assumes all files are numbered files with no folders
	highest_num = 0
	for filename in dirs:
		analyze_filename = regex.search(filename)

		if int(analyze_filename.group('numbering')) > highest_num:  # if the label number is higher than highest_num, set highest_num to label number
			highest_num = int(analyze_filename.group(3))
		else:
			# otherwise skip on to analyze the next filename
			pass

	# print(highest_num)

	return highest_num # return the highest number value

highest_label_num = highest_labelled_number(user_input_folder,prefix_regex2)



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

def process_file_lists(filename,filename_list,file_path_list,file_current_index):
	proc_file_list.append(filename) # append the file name into the proc_file_list
	proc_filePath_list.append(file_path_list[file_current_index]) # append the file path corresponding to the same index position as filename in filename_list

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

	print("The highest label number in the set is:  %i" % highest_label_num)

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

def rename_files(old_file_path,new_file_path):
	# use shutil.move to rename the file
	# shutil.move(old_path,new_path)

	try:
		for item in old_file_path:
		# item is the old file path
			get_item_index = old_file_path.index(item)
			
			if item == new_file_path[get_item_index]:
				print("The old file path was not replaced:  %s" % (item))
				pass
			else:
				print("The old file path replaced:  %s" % (item))
				print("The new file path is:  %s" % (new_file_path[get_item_index]))
				shutil.move(item,new_file_path[get_item_index])
	except Exception as e:
		print("There is an error in rename_files function.  The error is:  ")
		print(e)
		print("\n\n")
	else:
		pass

	

#####################################
# EXECUTION
#####################################

# analyze the files
analyze_files(user_input_folder,filename_list,file_path_list)

# start fixing the numbering
fix_numbering(proc_file_list,proc_filePath_list,prefix_regex2)

# complete the renaming file process
rename_files(proc_filePath_list,filePath_list_final)

# for testing
# for filename in proc_file_list:
# 	print(filename)

# for filepath in proc_filePath_list:
# 	print(filepath)

# print(file_list_final)
# print(filePath_list_final)

#####################################
# END EXECUTION
#####################################


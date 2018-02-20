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

# processing file name list
proc_file_list = []

# processing file name path list
proc_filePath_list = []

# we need the number of files in the use input directory so we know what the final number to use is

true_max_num = len(os.listdir(user_input_folder)) # actual upper limit of numbering unlike highest_labelled_number()
# print(max_num)

#####################################
# END VARIABLES
#####################################

def highest_labelled_number (user_input_folder,regex):
	dirs = os.listdir(user_input_folder) # assumes all files are numbered files with no folders
	highest_num = 0
	for filename in dirs:
		analyze_filename = regex.search(filename)

		if int(analyze_filename.group(3)) > highest_num:  # if the label number is higher than highest_num, set highest_num to label number
			highest_num = int(analyze_filename.group(3))
		else:
			# otherwise skip on to analyze the next filename
			pass

	# print(highest_num)

	return highest_num # return the highest number value

def store_file_dict(filename,filename_list,file_path_list,file_dict_master,file_current_index):
	# store the filename and its path in file_dict_master dictionary
	
	filename_path_value = file_path_list[file_current_index] # get the value or filename path at the same index position as filename_index
	# print(filename_path_value)
	
	file_dict_master[filename] = filename_path_value # if it matches, store it in a dict with the filename as the key and its filepath as the value

def process_file_lists(filename,filename_list,file_path_list,file_dict_master,file_current_index):
	proc_file_list.append(filename) # append the file name into the proc_file_list
	proc_filePath_list.append(file_path_list[file_current_index]) # append the file path corresponding to the same index position as filename in filename_list

def check_numbering(filename_list,file_path_list,regex,file_dict_master):
	# check files and locate numbering gaps
	# current_num = 1

	# for file in filename_list:
	# 	print(file)

	# need a loop within a loop
	# first we start at number 1 and cycle through all the files until we find 1
	# then we do it for 2
	# if we don't find 2 (or "n"), then we check if 3 exists ("n + 1")
	# if it does we re-name it to 2
	# then we continue
	
	max_num = highest_labelled_number(user_input_folder,prefix_regex2)
	# print("Highest label number is: %s" % (max_num))

	for num_pos in range(1,max_num+1): # we start at 1 not 0 and thus must use max_num + 1 as the upper limit
	# what happens if we have a lot of gaps and the max number range is really too high?  we would need to find the current numbering of the last file to get an accurate upper limit

		for file in filename_list:
			analyze_filename = regex.search(file)
			# print(analyze_filename)
			file_current_index = filename_list.index(file)
			# print("The current index of filename is %s" % (file_current_index))
			# file_plus_one_pos = file_current_index + 1
			# current_num = filename_list.index(file) + 1 # can't tie it to current index of file, it could be wrong, tie it to a separate counter
			
			# print(int(analyze_filename.group(3)))

			# if int(analyze_filename.group(3)) == (current_num):
			if int(analyze_filename.group(3)) == num_pos:
				# if the number of the filename matches the index number of its position + 1 (since index starts at 0 and we want to match 1 with 1 for example)
				
				# print(int(analyze_filename.group(3)))
				# print(num_pos)

				# store the filename and its path in file_dict_master dictionary
				
				# store_file_dict(file,filename_list,file_path_list,file_dict_master,file_current_index)
				
				# filename_path_value = file_path_list[file_current_index] # get the value or filename path at the same index position as filename_index
				# # print(filename_path_value)
				
				# file_dict_master[file] = filename_path_value # if it matches, store it in a dict with the filename as the key and its filepath as the value

				# print(file)
				# print(file_dict_master[file])

				# current_num += 1 # increment counter
				
				process_file_lists(file,filename_list,file_path_list,file_dict_master,file_current_index)

			else:
				# otherwise if it doesn't match at all
				# set the number to match the current index number
				fix_numbering(proc_file_list,proc_filePath_list,regex)

def analyze_files(foldername,filename_list,file_path_list,file_dict_master):
	# generate list of file names and corresponding list of paths to each of those file names that will be altered
	filename_list = fileTools.scanFile(foldername,file_path_list)

	# for testing
	# print("The file name list is:  ")

	# for filename in filename_list:
	# 	print(filename)
	
	# print("The file name path list is:  ")
	# for filename in file_path_list:
	# 	print(filename)
	
	# print(file_dict_master)
	# print("The file name and path dictionary:  ")
	# for key in file_dict_master:
	# 	print("The key is:  %s...  The value is:  %s" % (key,file_dict_master[key]))

	# for k, v in file_dict_master.items():
 #    print(k, v)

	# print(file_dict_master["spam001.txt"])
	
	

	check_numbering(filename_list,file_path_list,prefix_regex2,file_dict_master)

def fix_numbering(proc_file_list,proc_filePath_list,regex):
	# rename all later files after a gap is discovered so numbering is in sync
	# change the filename using regex substitution
	# then find its corresponding position on the file_path_list
	# use the new filename after substitution to do another regex sub to change its name entry in its file path in the file_path_list 
	
	max_num = highest_labelled_number(user_input_folder,prefix_regex2)

	for filename in proc_file_list:
		# if the filename's number matches (index + 1) do nothing
		# if the filename's number does not match (index + 1), grab the file right after it and rename it so that it does match (index + 1)
		pass

	pass # keep enabled until ready to test

#####################################
# EXECUTION
#####################################

# analyze_files(user_input_folder,folder_path_list,file_path_list)
analyze_files(user_input_folder,filename_list_f,file_path_list,file_dict_master)

# for testing
# for k, v in file_dict_master.items():
# 	print(k, v)

# for testing
# for filename in proc_file_list:
# 	print(filename)

# for filepath in proc_filePath_list:
# 	print(filepath)

#####################################
# END EXECUTION
#####################################


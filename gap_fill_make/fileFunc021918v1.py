# -*- coding: utf-8 -*-

# ! /usr/local/Cellar/python3/3.6.1

import os, re, shutil

#####################################
# SUGGESTED VARIABLES TO USE IN FILES USING THESE FUNCTIONS
#####################################

# get the absolute file path of the current working directory of program
abs_cwd_file_path = os.path.abspath('.') # set the destination file path to be the current working directory or cwd

# a list of all folders and subfolders to be analyzed
# folder_path_list = [] # a list to hold all finalized folder paths (not folder names)

# a list of all files to be analyzed
# file_path_list = [] # a list to hold all finalized folder paths (not folder names)

# dummy variables
# user_file_ext_input = "" # for functions taken from other programs

#####################################
# END SUGGESTED VARIABLES TO USE IN FILES USING THESE FUNCTIONS
#####################################

def find_abs_src_path(path,filename):
	# SOURCE FILE
	# get the directory path leading to the file name for later source copying
	# we need to do this rather than using `user_folder_input` otherwise we'll miss subfolders and get errors
	# use `os.path.join()` to create correct path rather than string concatenation
	# use os.path.abspath() to make sure it's an absolute path
	
	# src_file_path_name = os.path.abspath(os.path.join(user_folder_input,filename))
	src_file_path_name = os.path.abspath(os.path.join(path,filename))

	return src_file_path_name

def find_abs_dst_path(path,filename):
	# dst_file_path_name = os.path.join(search_result_path,filename + "_" + "copy")
	dst_file_path_name = os.path.join(path,filename) # use regex substitution to change the file name so that shutil.copyfile() will work as it won't work if the names are identical for some reason?

	return dst_file_path_name

def copy_file_sh(filename,src,dst):
	# COPY PROCESS
	# copy the files from their current location into a new folder (see Scratch file for thoughts on where new folder should be)

	print("Copying file: %s" % (filename))

	shutil.copyfile(src, dst)

def scanFolder(foldername_path,folder_path_list):
	# this function scans the parent folder and subfolders
	# it then adds them to a list so that its files can be scanned individually

	# `foldername_path` should actually be a string path to folder
		
	# as we get deeper and deeper into subfolders it should add onto the folder's path string that we pass to it so accuracy should be maintained

	dirs = os.listdir(foldername_path) # list all files of any kind (i.e. all file and folder names)

	foldername_list = [] # to be returned in case we want to work only with the name

	# folder_path_list = [] # a list to hold all finalized folder paths (not folder names)

	for file in dirs:
		# new_path = os.path.join(absPath,file) # creates a path to the file/folder
		new_path = os.path.join(foldername_path,file) # creates a path to the file/folder

		if os.path.isdir(new_path): #if the file is a folder
			folder_path_list.append(new_path) # add it to the list of folders with its full path name
			foldername_list.append(file)
		else:
			continue # otherwise skip and keep going

	return foldername_list

def scanFile(foldername_path, file_path_list):
	# the file scanner that gets all of the files and pushes them into a list after we get the full string path to it
	
	dirs = os.listdir(foldername_path) # list all files of any kind (i.e. all file and folder names)

	filename_list = [] # to be returned in case we want to work only with the name

	for file in dirs:
		# new_path = os.path.join(absPath,file) # creates a path to the file/folder
		new_path = os.path.join(foldername_path,file) # creates a path to the file/folder

		if os.path.isfile(new_path): #if the file is a file AND has regex match
			file_path_list.append(new_path) # add it to the list of folders with its full path name
			filename_list.append(file)
		else:
			continue # otherwise skip and keep going

	return filename_list


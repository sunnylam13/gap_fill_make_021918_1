# Scratch File

## Monday, February 19, 2018 3:53 PM

Possible file structure...  we have one file in /gap_fill_make for filling in gaps and another one for creating gaps.

We could create a 3rd execution .py program, importing the other 2 in order to combine the functions into one Py executon file.

For ease of import into the final combination function (`gap_fill_make_021918_1.py`) you'll want to wrap all of the code in the imported "fill" and "make" files in their own function.

We should assume that the "prefix" always uses letters...  it would make writing the regex for it a lot easier.

The prefix found using regex should be a group for later substitution.

For...

	spam001.txt

one could use either...

	(^[a-z]*) # matching 0 or more because some files have no prefix and are just 001.txt, https://regexr.com/3l1bg

however since this program specifically works with prefixed files and assuming the prefix is always letters and not anything mixed...

	(^[a-z]+) # matching 1 or more letters in the prefix, https://regexr.com/3l1bj

If it's prefixes like... 

	sp1em001.txt

You'd probably have to do it character by character...

	(^[a-z]{2}[0-9][a-z]+) # https://regexr.com/3l1bp

The program would have to know the exact prefix or you'd have to write code to analyze the more annoying cases.

The challenge with analyzing the numbers is that the format could vary greatly...

	spam001.txt

	spam0001.txt

	spam-0001.txt

We should assume the numbering is in the:

	spam001.txt

format for this program case...

If: 

	spam001.txt

	(^[a-z]+)(0*)([1-9]*)

you would use `group(3)` to get the number... (https://regexr.com/3l1dr)

You could use the regex to do both the prefix and the number analysis actually and skip using just `(^[a-z]+)` for example.


## Monday, February 19, 2018 4:55 PM

	## Testing

	mo_a1 = prefix_regex2.search("spam001.txt")
	print(mo_a1)
	# test groupings
	print(mo_a1.group(1))
	print(mo_a1.group(2))
	print(mo_a1.group(3))

results in

	<_sre.SRE_Match object; span=(0, 7), match='spam001'>
	spam
	00
	1

## Monday, February 19, 2018 6:45 PM

Just realized that the order of the file names and file paths in the Python lists isn't always the way you expect it...

	The file name list is:
	spam003.txt
	spam001.txt
	spam004.txt
	The file name path list is:
	../docs/testFolder1/spam003.txt
	../docs/testFolder1/spam001.txt
	../docs/testFolder1/spam004.txt

You'll see that the order is 3, 1, 4 rather than 1, 3, 4...

A more comprehensive gap fixer would figure out which one is first and then assign it to another list or dict first, so on and so forth.

The issue is that if you were a writer and you wanted to preserve the order of chapters for example, a loop with 3, 1, 4 to match 1, 2, 3 index positions and code like...

	def check_numbering(filename_list,file_path_list,regex):
		# check files and locate numbering gaps
		for file in filename_list:
			analyze_filename = regex.search(file)
			if int(analyze_filename.group(3)) == (filename_list.index(file) + 1):
				# if the number of the filename matches the index number of its position + 1 (since index starts at 0 and we want to match 1 with 1 for example)
				# if it matches, do nothing
				continue
			else:
				# set the number to match the current index number
				fix_numbering(filename_list,file_path_list,regex)

	def fix_numbering(filename_list,file_path_list,regex):
		# rename all later files after a gap is discovered so numbering is in sync
		# change the filename using regex substitution
		# then find its corresponding position on the file_path_list
		# use the new filename after substitution to do another regex sub to change its name entry in its file path in the file_path_list 
		pass

would result in the chapter order possibly being screwed up

for other situations where you don't care this would be fine

## Monday, February 19, 2018 7:06 PM

From what I can tell maybe using a dict isn't good...

What we need is to create an empty list with empty string values up to the length of the number of files in the analyzed directory.

As we analyze the files, we search for files with 1, if we find it we store it at the list[0] position of the list...  

We cycle through all possible numbers... 

And then we find out the problem is that also doesn't work too well because your list now has gaps however you need to rename the file in the next position.


## Monday, February 19, 2018 8:30 PM

Weirdly it seems every other file except 1 and 3 in the number order is in the right order...

## Monday, February 19, 2018 9:15 PM

	for num_pos in range(1,(max_num + 2)): # we start at 1 not 0 and thus must use max_num + 1 as the upper limit
	# what happens if we have a lot of gaps and the max number range is really too high?  we would need to find the current numbering of the last file to get an accurate upper limit

The issue is that the file numbering may actually be higher than the actual number of files which would screw up the loop...

Say you have 5 files from 001 to 006...  However your loop only goes to the max number of files which is 5...

However your loop needs to analyze the filename of ALL the files, which means that 006 is now outside of the loop with range of 1 to 5...  So now you've missed assessing a file.

So that means we need to use regex to find the number of the very last and/or highest numbered file.

## Tuesday, February 20, 2018 4:50 PM

> Remember that Python’s string literals also use a backslash followed by numbers to allow including arbitrary characters in a string, so be sure to use a raw string when incorporating backreferences in a RE. [Source](https://docs.python.org/3/howto/regex.html)

## Tuesday, February 20, 2018 5:27 PM

It seems we need to find and replace elements on the existing list before we do the moving.  Otherwise we throw an error.

## Tuesday, February 20, 2018 5:42 PM

	# if it matches the highest number we've analyzed, not necessarily the last index number i.e. 007
	# we need to account for the number of gap files as well to subtract with

The real issue here is that you might have a gap between 001 and 0062 and your final number is 0070 and there are only five files.  That means 70 has to change from 70 to file 005.

You need to figure out how to handle that situation.

Simple change it to the last number of the index of the filename path list as it has to be the last one anyone no matter what.

## Wednesday, February 21, 2018 10:25 AM

We're going to try and find the file number using a find command for lists.

	# try:
	#     b = a.index(7)
	# except ValueError:
	#     "Do nothing"
	# else:
	#     "Do something with variable b"

	# find the file with number 1
	# if you can't find it then, cycle through proc_file_list until you do
	# if you find it add it to the file_list_final,filePath_list_final
	# if you still can't find it, grab the file in the index + 1 position or the next file on the list and change it to be 1
	# rinse and repeat

## Wednesday, February 21, 2018 11:53 AM

We need to account for the case were the index is 0 and the new target number is 1.

There aren't many numbering schemes that start with file0000.txt.

## Wednesday, February 21, 2018 12:09 PM

Consider using match() or other methods to find the string filename that you want in a list.

[check if list item contains a string inside another string](https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string)

	>>> lst = ['abc-123', 'def-456', 'ghi-789', 'abc-456']
	>>> print filter(lambda x: 'abc' in x, lst)
	['abc-123', 'abc-456']
	You can also use a list comprehension.

	>>> [x for x in lst if 'abc' in x]

hmm...

	target_matches = filter(lambda x: filename in x, proc_file_list) # search for proc_file_list[current_filename_index] value, this is a list, convert to string for use

## Friday, February 23, 2018 9:56 AM

Gap Maker Program

Actions

Get the user input folder with list of numbered files.

Get the user input on where they want to insert the gap.

Will it be between 1 and 2 or 5 and 6?

Best way is to ask for the number they would like to insert it after.  Technically this covers all situations more easily then "before #" because you can't do "before #" if you want to insert anything after the "last number" however you can always insert after.

Unless the user wants to insert a number before 1 (first file) to create a new first file.

This means we'll need to take the input of "insert before" or "insert after" or create a choice menu for those options plus ask the user for the file they wish to insert before/after.

You could make this a one line input if you write regex to find "insert before" and "insert after" and the number and use regex groups so you can analyze each part for internal logic.

Scan the user input folder for a list of numbered files.  Store all the file names in a new list.

Get the directory path for the folder to create file paths for the original list of numbered files.

Create file paths for the original list of numbered files.  Store all the file paths in the original file path list.

Go to the index position of the number user entered.

If they used "insert before", change the original file name at the position and every file after by increasing it's label number by +1.  Append/store the change in the new file name list.

If they used "insert after", don't change the original file name at the position.  Instead change every file after by increasing its label number by +1. Append/store the change in the new file name list.

NOTE:  in no case should the index position ever change only the filename number label.

Now change the names of the original file path list to that of the new file path list.  Store all the file paths in the new file path list.

Using the new file name list, create file paths for the new list of numbered files.  Use shutil.move() to change the files specified by the file paths from the original to the new.


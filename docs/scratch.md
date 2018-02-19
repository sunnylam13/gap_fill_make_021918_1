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





# Gap Filler Maker

This program finds all files with a given prefix in a single folder and locates any gaps in numbering (i.e. spam001.txt, spam003.txt, missing spam002.txt)...

Alternatively, this program inserts gaps into numbered files so that a new file can be added.

## Actions

* figure out what the given prefix is using regex and the groups for substitution

* analyze the number of said files and determine what the gap is

* fix the gap by renaming the later files so that the gap is closed

## Status

incomplete

## Test Folder

	../docs/testFolder1

The zip file archive of it is the original that should be used.  

Just unzip it and run the program.

## Regex

https://regexr.com/3l545 # `(^[a-z]+)(0*)([1-9]*)(\..*$)`

## Tags

gap, filenames, renaming

## References

[Iterating Key Value Pairs in a Py3 Dict](https://stackoverflow.com/questions/26660654/how-do-i-print-the-key-value-pairs-of-a-dictionary-in-python/26660785)

[Add Key Value Pair to Dict](https://stackoverflow.com/questions/3776275/how-to-add-key-value-pair-to-dictionary/28380174)

[Good Reference on Using Groups for Regex and String Substitution](https://docs.python.org/3/howto/regex.html)

[check if a value exists in a list](https://stackoverflow.com/questions/7571635/fastest-way-to-check-if-a-value-exist-in-a-list)

[check if list item contains a string inside another string](https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string)


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

## Tags

gap, filenames, renaming

## References


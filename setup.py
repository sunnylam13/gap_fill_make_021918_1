try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'This program finds all files with a given prefix in a single folder and locates any gaps in numbering (i.e. spam001.txt, spam003.txt, missing spam002.txt)...  Also gives the option to insert gaps into numbered files so that a new file can be added.',
	'author': 'Sunny Lam',
	'url': 'https://github.com/sunnylam13/gap_fill_make_021918_1',
	'download_url': 'https://github.com/sunnylam13/gap_fill_make_021918_1',
	'author_email': 'sunny.lam@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['os, re, shutil'],
	'scripts': [],
	'name': 'Gap Filler Maker'
}

setup(**config)
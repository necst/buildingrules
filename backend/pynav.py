## pyProjectNavigator - v0.1
#
# Descrition:  
# This script finds all the method name (given a module or a class) inside a python project
#
# Author: Alessandro A. Nacci
# mail: alenacci@gmail.com

import os
import sys

if len(sys.argv) != 3:
	print "Usage:   python pynav.py [root_dir] [module_name]"
	print "Example: python pynav.py ./ users"
	sys.exit(-1)

rootdir = sys.argv[1]
className = sys.argv[2]

for root, subFolders, files in os.walk(rootdir):
	for file in files:
		if className in file and file.endswith(".py"):

			print " - " + file

			file_path = os.path.join(root,file)
			f = open(file_path)
			lines = f.readlines()
			f.close()

			methodList = []
			for line in lines:
				if line.strip().startswith("def "):
					methodList.append(line.strip())
					
			methodList.sort()

			for method in methodList:
				print " |---- + " + method

			print 
			print
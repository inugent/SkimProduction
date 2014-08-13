#!/usr/bin/env python

import os
import glob

print "Adding two lines to crab_*/job/CMSSW.sh for proper environment setup on grid"

overwriteFile = False

dirs = glob.glob("*/job/")

for i in range(len(dirs)):
	filePath = os.path.abspath(".")+"/"+dirs[i]+"CMSSW.sh"

	file = open(filePath,"r")
	input = file.readlines()
	file.close()

	for j in range(len(input)):
		if("eval `scram runtime -sh | grep -v SCRAMRT_LSB_JOBNAME`" in input[j]):
			if ("scramv1 setup lhapdffull" in input[j+1]) or ("scramv1 b" in input[j+2]):
				overwriteFile = False
				print "File already contains proper environment setup. Breaking."
				break
			else:
				input.insert(j+1,"scramv1 setup lhapdffull\n")
				input.insert(j+2,"scramv1 b\n")
				overwriteFile = True
				print "Added lines."
				break
	if overwriteFile:
		file = open(filePath,"w")
		for line in input:
			file.write(line)
		file.close()
		print "File "+dirs[i]+"CMSSW.sh"+" overwritten."
	else:
		print "File "+dirs[i]+"CMSSW.sh"+" not overwritten."

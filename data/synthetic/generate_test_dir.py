'''
Read in test source definition
create new directory for test inputs
'''

import os
from shutil import copyfile
from os.path import join, basename, dirname

#input file
find = 'shadow'
replace = 'test_' + find

infile = 'sources/source_' + find + '_test.txt'
outbase = 'images/test_' + find + '/'


lines = [line.rstrip('\n') for line in open(infile)]

for line in lines:
	# line is the path
      # get directory of bw mask

  # generate scene directory
  split = line.split("/")
  dir_o = outbase + split[1]
  print 'output dir ' + dir_o	
  try: os.makedirs(dir_o)
  except: pass

  # get dest path
  dest = line.replace(find, replace)
  print line

  print 'src: ' + line
  print 'dest: ' + dest

  # copy the file
  copyfile('./images/' + line, './images/' + dest)
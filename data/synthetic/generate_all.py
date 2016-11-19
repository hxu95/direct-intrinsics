import os

#start in synthetic/ dir
# dir structure of synthetic/
	# noshadow/
	# shadow/
# elems = ['albedo_defect_mask', 'albedo', 'clean']
elems = ['shadows', 'noshadows']
prefix = './images/'

# write all filenames in directories into outdir
for elem in elems:
    outfile  = './sources/source_{}_full.txt'.format(elem)
    print outfile

    with open(outfile, "w") as a:
        for path, subdirs, files in os.walk('./images/{}'.format(elem)):
            for filename in files:
                f = os.path.join(path, filename)
                if f.startswith(prefix):
                    a.write(f[len(prefix):] + os.linesep) 
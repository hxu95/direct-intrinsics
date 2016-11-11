import os

elems = ['albedo_defect_mask', 'albedo', 'clean', 'shading', 'RS']
prefix = '/home/hxu/direct-intrinsics-final-project/data/sintel/images/'
for elem in elems:
    outfile  = '/home/hxu/direct-intrinsics-final-project/data/sintel/sources/source_{}_full.txt'.format(elem)
    print outfile

    with open(outfile, "w") as a:
        for path, subdirs, files in os.walk('/home/hxu/direct-intrinsics-final-project/data/sintel/images/{}'.format(elem)):
            for filename in files:
                f = os.path.join(path, filename)
                if f.startswith(prefix):
                    a.write(f[len(prefix):] + os.linesep) 

                #print f
                
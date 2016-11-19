from os.path import join, dirname
import sys
#manual path definition
#sys.path.append('/home/hxu/caffe/python')
import matplotlib.pyplot as plt
import cv2
import numpy as np
import caffe
import os
# walk through synthetic images with shadows and remove shadows
# results go into directory with the same filename

import direct_intrinsics as di

project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
#project_path = '/home/hxu/di-final/'

# not sure these paths are right
# point to generated data with shadows
input_path = 'data/synthetic/images/shadow/'

#for cvpr
#input_path = 'data/cvpr11/shadow'

shadow_path = 'shadow/'
result_path = 'results/'

# Load net
#modelfile = 'mit_final_barron_train.caffemodel'
# TODO: check paths here
modelfile = project_path + 'training/snapshot__iter_5000.caffemodel'
net = caffe.Net('direct_intrinsics_without_shading.prototxt', modelfile, caffe.TEST)

# get list of file names and paths to them in the input
path = project_path + input_path
print path
list_of_files = {}

#walk through shadows, get all images and subdirectories
for (dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        #list_of_files[filename] = os.sep.join([dirpath, filename])
        print filename
        imgpath = os.sep.join([dirpath, filename])
        print imgpath

        path_o = imgpath.replace(shadow_path, result_path)

        #path_o = join(input_path, result_path, paths[sc][i].replace('clean/', ''))
        dir_o = dirname(path_o)
        print path_o
        print dir_o
        if not os.path.isdir(dir_o):
            os.makedirs(dir_o)

        # read in image
        img = cv2.imread(imgpath)

        # Predict
        result = di.predict(net, img)

        # Display results
        '''
        plt.figure()
        plt.title('input')
        plt.imshow(di.bgr2rgb(img))
        plt.figure()
        plt.title('albedo')
        plt.imshow(result)
        plt.figure()
        plt.show()
        '''
        
        # save the result
        imsave(path_o, result)
from os.path import join, dirname
import sys
#manual path definition
#sys.path.append('/home/hxu/caffe/python')
import matplotlib.pyplot as plt
import cv2
import numpy as np
# TODO: 
# import caffe
import os

# walk through synthetic images with shadows and remove shadows
# results go into directory data/results with the same filename

import direct_intrinsics as di

# project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
#project_path = '/home/hxu/di-final/'
project_path = '/home/hxu/6.869/direct-intrinsics-final-project/'
# point to generated data with shadows
img_path = project_path + 'data/synthetic/images/'

shadow_path = 'shadow/'
result_path = 'results/'

input_path = img_path + shadow_path

path_r = img_path + result_path
print 'result path: ' + path_r
#for cvpr
#input_path = 'data/cvpr11/shadow'
print os.path.exists(path_r)
if not os.path.exists(path_r):
    os.makedirs(path_r)
else:
    print "EXISTS " + path_r

# Load net
# modelfile = 'mit_final_barron_train.caffemodel'
# TODO: point to the prototxt and model that we want to use
modelfile = project_path + 'training/snapshot__iter_5000.caffemodel'
proto = 'direct_intrinsics_without_shading.prototxt'

# TODO: load the net
# net = caffe.Net(proto, modelfile, caffe.TEST)

# get list of file names and paths to them in the input
#path = project_path + input_path
print 'input path: ' + input_path
list_of_files = {}

#walk through shadows, get all images and subdirectories
for (dirpath, dirnames, filenames) in os.walk(input_path):
    for filename in filenames:
        #list_of_files[filename] = os.sep.join([dirpath, filename])
        imgpath = os.sep.join([dirpath, filename])
        # print imgpath

        path_o = imgpath.replace(shadow_path, result_path)

        #path_o = join(input_path, result_path, paths[sc][i].replace('clean/', ''))
        dir_o = dirname(path_o)


        # dir_o = join(dir_out, basename(dir_scene))
        try: 
            os.makedirs(dir_o)
            print 'output path: ' + path_o
            print 'output dirname: ' + dir_o
        except:
            pass

        # read in image
        # img = cv2.imread(imgpath)

        # Predict
        # result = di.predict(net, img)

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
        # imsave(path_o, result)
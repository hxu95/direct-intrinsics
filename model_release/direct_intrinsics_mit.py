'''
Do prediction and channel prediction for all images in test
'''
# Set python path here
import sys
#manual path definition
#sys.path.append('/home/hxu/caffe/python')
import matplotlib.pyplot as plt
import cv2
import numpy as np
import caffe
import direct_intrinsics as di

import os, sys, traceback
from glob import glob
from os.path import join, basename, dirname

# project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
project_path = '/home/hxu/di-final/'
# In[3]:

# Load net
#modelfile = 'mit_final_barron_train.caffemodel'

# modelfile = project_path + 'training/snapshot_shadow_removal_more_lambda00_30000.caffemodel'
modelfile = project_path + 'training/snapshot_shadow_removal_room_34000.caffemodel'
net = caffe.Net('direct_intrinsics_without_shading.prototxt', modelfile, caffe.TEST)

# synthetic or not - true is synthetic, false is CVPR 
scenes = False

root = None
dir_shadow = None
dir_predicted = None 
dir_channel = None
# synthetic
if scenes:
  root = 'data/synthetic/images/'
  dir_shadow = project_path + root + 'test_shadow'

  dir_predicted = project_path + root +'test_predicted'

  dir_channel = project_path + root + 'test_channel_prediction'
else:
  # cvpr 11
  # root = 'data/cvpr11/'
  root = 'data/cvpr10/'
  dir_shadow = project_path + root + 'shadow/'

  dir_predicted = project_path + root + 'test_predicted/'

  dir_channel = project_path + root + 'test_channel_prediction/'


# do synthetic data with scenes
if scenes:
  for dir_scene in sorted(glob(join(dir_shadow, '*'))):
      for path_shadow in sorted(glob(join(dir_scene, '*.png'))):
        print 'input: ' + path_shadow
        img = cv2.imread(path_shadow)

        if img is None:
          continue

        # Predict by Direct intrinsics CN
        a = di.predict(net, img)

        # try to write the predicted image
        dir_o = join(dir_predicted, basename(dir_scene))
        try: os.makedirs(dir_o)
        except: pass

        # save the prediction
        path_result = join(dir_o, basename(path_shadow))
        plt.imsave(path_result, a)

        print 'predicted: ' + path_result

        # make sure the dimensions match
        a = cv2.imread(path_result)
        a = cv2.resize(a, (img.shape[1], img.shape[0])) 
        if a.shape != img.shape:
          print 'dimensions do not match!'
          print 'a.shape: ' + str(a.shape)
          print 'img.shape: ' + str(img.shape)
          continue

        shadow = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        in_l, in_a, in_b = cv2.split(shadow)
          
        aLAB = cv2.cvtColor(a, cv2.COLOR_BGR2LAB)
        out_l, _, _ = cv2.split(a)

        # print out_l
        # print in_l
        '''
        print 'shapes'
        print out_l.shape
        print in_a.shape
        priXnt in_b.shape

        print 'sizes'
        print out_l.size
        print in_a.size
        print in_b.size
        '''
        predicted = cv2.merge([out_l, in_a, in_b])
        predicted = cv2.cvtColor(predicted, cv2.COLOR_LAB2RGB)

        # try to write the channel predicted
        dir_o = join(dir_channel, basename(dir_scene))
        try: os.makedirs(dir_o)
        except: pass

        # save the channel reconstruction
        path_result = join(dir_o, basename(path_shadow))
        plt.imsave(path_result, predicted)

        print 'channel prediction: ' + path_result

#cvpr
else:
  for filename in os.listdir(dir_shadow):
    # make sure it is a jpg
    if not filename.endswith('.jpg'):
      continue
    
    path_shadow = dir_shadow + filename
    print 'input: ' + path_shadow
    img = cv2.imread(path_shadow)

    if img is None:
      continue

    # Predict by Direct intrinsics CN
    a = di.predict(net, img)

    # try to write the predicted image
    try: os.makedirs(dir_predicted)
    except: pass

    # save the prediction
    path_result = dir_predicted + filename
    plt.imsave(path_result, a)

    print 'predicted: ' + path_result

    # make sure the dimensions match
    a = cv2.imread(path_result)
    a = cv2.resize(a, (img.shape[1], img.shape[0])) 
    if a.shape != img.shape:
      print 'dimensions do not match!'
      print 'a.shape: ' + str(a.shape)
      print 'img.shape: ' + str(img.shape)
      continue

    shadow = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    in_l, in_a, in_b = cv2.split(shadow)
      
    aLAB = cv2.cvtColor(a, cv2.COLOR_BGR2LAB)
    out_l, _, _ = cv2.split(a)

    predicted = cv2.merge([out_l, in_a, in_b])
    predicted = cv2.cvtColor(predicted, cv2.COLOR_LAB2RGB)

    # try to write the channel predicted
    try: os.makedirs(dir_channel)
    except: pass

    # save the channel reconstruction
    path_result = dir_channel + filename
    plt.imsave(path_result, predicted)

    print 'channel prediction: ' + path_result
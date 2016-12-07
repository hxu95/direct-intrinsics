import os, sys, traceback
from glob import glob
import matplotlib.pyplot as plt
from os.path import join, basename, dirname
import matplotlib.image as mpimg
import numpy as np
# from scipy.misc import imread, imsave
import cv2



# project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
project_path = '/home/hxu/di-final/'
# project_path = '/home/hxu/6.869/direct-intrinsics-final-project/'
# not sure these paths are right
# point to generated data with shadows
# result_path = 'data/synthetic/images/results/'
result_path = 'data/cvpr11/shadow'
noshadow_path = 'data/cvpr11/noshadow'
dir_out = 'data/cvpr11/shadowmask'

# path to folders for results and ground truth
# in the synthetic case they are 1:1
shadow_path = project_path + result_path
truth_path = project_path + noshadow_path
out_path = project_path + dir_out
print shadow_path
print truth_path

# initialize dicts of scene/filename -> abs path
shadow_dict = {}
truth_dict = {}

# first do the ground truth
# prefixes should be unique
for (dirpath, dirnames, filenames) in os.walk(truth_path):
    for filename in filenames:
        # key = prefix
        key = filename.split("_")[0]

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        truth_dict[key] = value

'''
        print filename
        print key
        print value
'''
print truth_dict

# now do the shadow
for (dirpath, dirnames, filenames) in os.walk(shadow_path):
    for filename in filenames:
        # key = prefix
        key = filename.split("_")[0]

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        # already exists in the dict
        # can be many to one
        if shadow_dict.get(key, None) is not None:
            shadow_dict[key].append(value)
        else:
            shadow_dict[key] = [value]


cumulative_rmse = 0
cumulative_ssim = 0
count = 0
# check that they are the same size
assert len(shadow_dict) == len(truth_dict)

total_error = 0

# iterate over dictionary
for key in truth_dict:
    #make sure we have a match
    assert key in shadow_dict
    gt_file = truth_dict[key]
    print 'truth: {}'.format(gt_file)
    gt_img = cv2.imread(gt_file)

    if gt_img is None:
        continue

    
    # path_noshadow = join(dir_noshadow, f)
    # print path_noshadow
    #path_noshadow = join(path_noshadow, basename(path_shadow))
    # noshadow = cv2.imread(path_noshadow)
    noshadow = cv2.cvtColor(gt_img, cv2.COLOR_BGR2LAB)
    noshadow_l_channel, _, _ = cv2.split(noshadow)
    # otherwise, run through the shadows
    # get comparisons

    files = shadow_dict[key]
    for exp_file in files:
        
        count = count + 1

        # read in the images - can also read in as greyscale?
        # to_grayscale(imread(file1).astype(float))

        exp_img = cv2.imread(exp_file)

        # convert to LAB
        shadow = cv2.cvtColor(exp_img, cv2.COLOR_BGR2LAB)
        shadow_l_channel, _, _ = cv2.split(shadow)

        # subtract channels?
        result = noshadow_l_channel - shadow_l_channel

        #invert
        # result = (255 - result)

        # account for wraparound
        result[result > 220] = 0

        # small distances -> no difference
        result[result < 60] = 0

        # set non-shadow to black?
        result[result > 0] = 255

        # not sure why we have to invert but we do, i guess
        if basename(exp_file).startswith('a'):
            print 'starts with a'
            result = (255 - result)

        # dir_o = join(dir_out, basename(dir_scene))
        try: os.makedirs(out_path)
        except: pass

        print 'path_shadow: ' + exp_file
        path_result = join(out_path, basename(exp_file))
        print 'path_result ' + path_result
    
        # result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # result = (255-gray_image)

        # assert np.array_equal(np.array(noshadow), np.array(shadow - result))
        cv2.imwrite(path_result, result)
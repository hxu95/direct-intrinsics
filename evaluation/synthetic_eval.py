# evaluate synthetic dataset results from net against generated ground truth
from os.path import join, dirname

# to do evaluation - mse or ssim?
# from skimage.measure import structural_similarity as ssim

from util import rmse

import sys, cv2
import numpy as np
import os

# path to direct intrinsics folder 
# project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
project_path = '/home/hxu/di-final/'

# not sure these paths are right
# point to generated data with shadows
# result_path = 'data/synthetic/images/results/'
result_path = 'data/synthetic/images/shadow/'
noshadow_path = 'data/synthetic/images/noshadow/'

# path to folders for results and ground truth
# in the synthetic case they are 1:1

# path to experimental results
experiment_path = project_path + result_path

# path to ground truth
truth_path = project_path + noshadow_path

print experiment_path
print truth_path

# initialize dicts of scene/filename -> abs path
experiment_dict = {}
truth_dict = {}

# first do the ground truth
for (dirpath, dirnames, filenames) in os.walk(truth_path):
    for filename in filenames:
        # get the scene that this thing is in
        _, scene = os.path.split(dirpath)
        # print scene

        # key = scene/filename
        key = os.sep.join([scene, filename])

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        truth_dict[key] = value

'''
        print filename
        print key
        print value
'''
print truth_dict


# now do the experiment
for (dirpath, dirnames, filenames) in os.walk(experiment_path):
    for filename in filenames:
        # get the scene that this thing is in
        _, scene = os.path.split(dirpath)
        # print scene

        # key = scene/filename
        key = os.sep.join([scene, filename])

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        experiment_dict[key] = value

'''
        print filename
        print key
        print value
'''
print experiment_dict

# check that they are the same size
assert len(experiment_dict) == len(truth_dict)

total_error = 0

# iterate over dictionary
for key in truth_dict:
    #make sure we have a match
    assert key in experiment_dict
    gt_file = truth_dict[key]
    exp_file = experiment_dict[key]
    print 'truth: {}'.format(gt_file)
    print 'experiment: {}'.format(exp_file)


'''
    # get paths of images


    # read in the images - can also read in as greyscale?
    # to_grayscale(imread(file1).astype(float))
    gt_img = imread(gt_file)
    exp_img = imread(exp_file)

    #truth, experiment
    r = rmse(gt_img, exp_img)
    # r = sqrt(mean_squared_error(gt_img, exp_img))
    # can also use structural similarity
    # s = ssim(gt_img, exp_img)

    # add to total
    total_error += r

# report average difference
print float(diff) / float(len(truth_dict))

'''
# evaluate cvpr results against ground truth
from os.path import join, dirname

# to do evaluation - mse or ssim?
# from skimage.measure import structural_similarity as ssim
from util import rmse

import sys
import numpy as np
import os

# project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
project_path = '/home/hxu/di-final/'

# not sure these paths are right
# point to generated data with shadows
# result_path = 'data/synthetic/images/results/'
result_path = 'data/cvpr11/shadow'
noshadow_path = 'data/cvpr11/noshadow'

# path to folders for results and ground truth
# in the synthetic case they are 1:1
experiment_path = project_path + result_path
truth_path = project_path + noshadow_path

print experiment_path
print truth_path

# initialize dicts of scene/filename -> abs path
experiment_dict = {}
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


# now do the experiment
for (dirpath, dirnames, filenames) in os.walk(experiment_path):
    for filename in filenames:
        # key = prefix
        key = filename.split("_")[0]

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        # already exists in the dict
        # can be many to one
        if experiment_dict.get(key, None) is not None:
            experiment_dict[key].append(value)
        else:
            experiment_dict[key] = [value]

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
    print 'truth: {}'.format(gt_file)

    # get comparisons
    files = experiment_dict[key]
    for file in files:
        print 'experiment: {}'.format(file)


'''
    # get paths of images
    exp_file = experiment_dict[file]

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
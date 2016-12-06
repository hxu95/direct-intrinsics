# evaluate synthetic dataset results from net against generated ground truth
from os.path import join, dirname

# from skimage.measure import structural_similarity as ssim

from util import rmse #, ssim, msssim

# skimage installation instructions
# http://stackoverflow.com/questions/38087558/import-error-no-module-named-skimage
from skimage.measure import compare_ssim as compare_ssim
# deprecated?
# from skimage.measure import structural_similarity as compare_ssim
from skimage import color

import matplotlib.image as mpimg
import sys, cv2
import numpy as np
import os

# path to direct intrinsics folder 
# project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
project_path = '/home/hxu/di-final/'
# project_path = '/home/hxu/6.869/direct-intrinsics-final-project/'


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
# print truth_dict


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

# check that they are the same size
assert len(experiment_dict) == len(truth_dict)

cumulative_rmse = 0
cumulative_ssim = 0

# iterate over dictionary
for key in experiment_dict:
    #make sure we have a match
    assert key in truth_dict

    # get matching files
    gt_file = truth_dict[key]
    exp_file = experiment_dict[key]
    print 'truth: {}'.format(gt_file)
    print 'experiment: {}'.format(exp_file)

    # read in the images - can also read in as greyscale?
    # to_grayscale(imread(file1).astype(float))
    gt_img = cv2.imread(gt_file)
    exp_img = cv2.imread(exp_file)

    if gt_img is None or exp_img is None:
        continue

    #truth, experiment
    assert gt_img.shape == exp_img.shape
    r = rmse(gt_img, exp_img)
    # r = sqrt(mean_squared_error(gt_img, exp_img))
    # can also use structural similarity
    # have to convert to gray: http://stackoverflow.com/questions/32077285/ssim-image-compare-error-window-shape-incompatible-with-arr-in-shape
    img1 = color.rgb2gray(gt_img)
    img2 = color.rgb2gray(exp_img)
    s = compare_ssim(img1, img2)

    # add to total
    cumulative_rmse += r
    cumulative_ssim += s

# report average difference
print 'RMSE'
print float(cumulative_rmse) / float(len(truth_dict))
print 'SSIM'
print float(cumulative_ssim) / float(len(truth_dict))
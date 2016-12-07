# evaluate synthetic dataset results from net against generated ground truth
from os.path import join, dirname

from util import rmse #, ssim, msssim

from skimage import color

import sys, cv2
import numpy as np
import os

# path to direct intrinsics folder 
# project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
# project_path = '/home/hxu/di-final/'
project_path = '/home/hxu/6.869/direct-intrinsics-final-project/'


# point to generated data with shadows
# result_path = 'data/synthetic/images/results/'

# path to generated shadow masks
# result_path = 'data/synthetic/images/generated_mask/'
result_path = 'data/synthetic/images/greyscale_shadowmask/'

# ground truth
noshadow_path = 'data/synthetic/images/bw_shadowmask/'

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

cumulative_diff = 0

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

    # in greyscale
    exp_mask = cv2.cvtColor(exp_img, cv2.COLOR_BGR2LAB)
    exp_l_channel, _, _ = cv2.split(exp_mask)

    #convert into bw
    # thresholding less than
    exp_l_channel[exp_l_channel < 50] = 0

    # everything else to white
    exp_l_channel[exp_l_channel > 0] = 255

    # print 'exp_l'
    # print exp_l_channel
    # bw mask
    gt_mask = cv2.cvtColor(gt_img, cv2.COLOR_BGR2LAB)
    gt_l_channel, _, _ = cv2.split(gt_mask)

    # print 'gt_l'
    # print gt_l_channel

    assert gt_l_channel.size == exp_l_channel
    # add to total
    diff = np.sum(np.array(gt_l_channel) == np.array(exp_l_channel)) / float(gt_l_channel.size)
    cumulative_diff += diff

    # break

# report average difference
print 'Average difference (%)'
print float(cumulative_diff) / float(len(truth_dict))
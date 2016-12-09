# evaluate cvpr results against ground truth
from os.path import join, dirname

# to do evaluation - mse or ssim?
from skimage.measure import structural_similarity as ssim
from skimage import color
from util import rmse
import sys
import numpy as np
import cv2
import os

# project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
project_path = '/home/hxu/di-final/'
# project_path = '/home/hxu/6.869/direct-intrinsics-final-project/'
# not sure these paths are right
# point to generated data with shadows
# result_path = 'data/synthetic/images/results/'

# generated shadow masks from CNN
# result_path = 'data/cvpr11/shadow'
root = 'data/cvpr10/'
result_path = root + 'shadowmask'

# gt

noshadow_path = root + 'gt_shadowmask'

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
        # key = filename.split("_")[0]

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        truth_dict[filename] = value

# now do the experiment
# prefixes may not be unique
for (dirpath, dirnames, filenames) in os.walk(experiment_path):
    for filename in filenames:
        # value = path to this image
        value = os.sep.join([dirpath, filename])

        # already exists in the dict
        # can be many to one
        experiment_dict[filename] = value


cumulative_diff = 0
count = 0
# check that they are the same size
assert len(experiment_dict) == len(truth_dict)
print truth_dict
print experiment_dict

# iterate over dictionary
for key in truth_dict:
    #make sure we have a match
    print key
    assert key in experiment_dict
    gt_file = truth_dict[key]
    
    print 'truth: {}'.format(gt_file)
    gt_img = cv2.imread(gt_file)

    # bw mask
    gt_mask = cv2.cvtColor(gt_img, cv2.COLOR_BGR2LAB)
    gt_l_channel, _, _ = cv2.split(gt_mask)

    if gt_img is None:
        continue

    count = count + 1

    # get matching files
    exp_file = experiment_dict[key]
    print 'experiment: {}'.format(exp_file)

    # read in the images - can also read in as greyscale?
    # to_grayscale(imread(file1).astype(float))

    exp_img = cv2.imread(exp_file)

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


    assert gt_l_channel.size == exp_l_channel.size
    # add to total
    diff = np.sum(np.array(gt_l_channel) == np.array(exp_l_channel)) / float(gt_l_channel.size)
    cumulative_diff += diff


# report average difference
print 'Average accuracy (%)'
print (float(cumulative_diff) / float(count)) * 100
# evaluate synthetic dataset results from net against generated ground truth
from os.path import join, dirname

from util import rmse #, ssim, msssim

from skimage import color

import sys, cv2
import numpy as np
import os

# path to direct intrinsics folder 
# project_path = '/afs/csail.mit.edu/u/y/ylkuo/project/cv_final/direct-intrinsics/'
project_path = '/home/hxu/di-final/'
# project_path = '/home/hxu/6.869/direct-intrinsics-final-project/'


# point to generated data with shadows
# result_path = 'data/synthetic/images/results/'

# path to generated shadow masks
# result_path = 'data/synthetic/images/generated_mask/'
img_root = 'data/synthetic/images/'
result_greyscale_path = project_path + img_root + 'greyscale_shadowmask/'
result_bw_path = project_path + img_root + 'bw_shadowmask/'

# ground truth
gt_greyscale_path = project_path + img_root + 'gt_greyscale_shadowmask/'
gt_bw_path =  project_path + img_root + 'gt_bw_shadowmask/'

# initialize dicts of scene/filename -> abs path
exp_grey_dict = {}
exp_bw_dict = {}
gt_grey_dict = {}
gt_bw_dict = {}

# first do greyscale experimental
for (dirpath, dirnames, filenames) in os.walk(result_greyscale_path):
    for filename in filenames:
        # get the scene that this thing is in
        _, scene = os.path.split(dirpath)
        # print scene

        # key = scene/filename
        key = os.sep.join([scene, filename])

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        exp_grey_dict[key] = value

# bw experimental
for (dirpath, dirnames, filenames) in os.walk(result_bw_path):
    for filename in filenames:
        # get the scene that this thing is in
        _, scene = os.path.split(dirpath)
        # print scene

        # key = scene/filename
        key = os.sep.join([scene, filename])

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        exp_bw_dict[key] = value

# grey truth
for (dirpath, dirnames, filenames) in os.walk(gt_greyscale_path):
    for filename in filenames:
        # get the scene that this thing is in
        _, scene = os.path.split(dirpath)
        # print scene

        # key = scene/filename
        key = os.sep.join([scene, filename])

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        gt_grey_dict[key] = value

# bw truth
for (dirpath, dirnames, filenames) in os.walk(gt_bw_path):
    for filename in filenames:
        # get the scene that this thing is in
        _, scene = os.path.split(dirpath)
        # print scene

        # key = scene/filename
        key = os.sep.join([scene, filename])

        # value = path to this image
        value = os.sep.join([dirpath, filename])

        gt_bw_dict[key] = value

# check that they are the same size
# assert len(experiment_dict) == len(truth_dict)
assert len(exp_bw_dict) == len(exp_grey_dict)
cumulative_accuracy = 0
cumulative_rmse = 0

# iterate over dictionary
for key in exp_grey_dict:
    #make sure we have a match
    assert key in exp_bw_dict
    assert key in gt_grey_dict
    assert key in gt_bw_dict

    # get matching files
    exp_grey_file = exp_grey_dict[key]
    exp_bw_file = exp_bw_dict[key]
    gt_grey_file = gt_grey_dict[key]
    gt_bw_file = gt_bw_dict[key]

    print 'exp grey: {}'.format(exp_grey_file)
    print 'exp bw: {}'.format(exp_bw_file)
    print 'gt grey: {}'.format(gt_grey_file)
    print 'gt bw: {}'.format(gt_bw_file)

    # read in the images - can also read in as greyscale?
    # to_grayscale(imread(file1).astype(float))
    exp_grey_img = cv2.imread(exp_grey_file)
    exp_bw_img = cv2.imread(exp_bw_file)
    gt_grey_img = cv2.imread(gt_grey_file)
    gt_bw_img = cv2.imread(gt_bw_file)

    # make sure we have a file
    if exp_grey_img is None or exp_bw_img is None or gt_grey_img is None or gt_bw_img is None:
        continue

    # reshape if necessary
    if exp_grey_img.shape != gt_grey_img.shape:
        exp_grey_img = cv2.resize(exp_grey_img, (gt_grey_img.shape[1], gt_grey_img.shape[0])) 

    if exp_bw_img.shape != gt_bw_img.shape:
        exp_bw_img = cv2.resize(exp_bw_img, (gt_bw_img.shape[1], gt_bw_img.shape[0])) 


    # rmse on greyscale masks
    r = rmse(exp_grey_img, gt_grey_img)
    cumulative_rmse += r

    '''
    #convert into bw
    # thresholding less than
    exp_l_channel[exp_l_channel < 50] = 0

    # everything else to white
    exp_l_channel[exp_l_channel > 0] = 255
    '''

    # read in and convert 
    exp_mask = cv2.cvtColor(exp_bw_img, cv2.COLOR_BGR2LAB)
    exp_l_channel, _, _ = cv2.split(exp_mask)

    gt_mask = cv2.cvtColor(gt_bw_img, cv2.COLOR_BGR2LAB)
    gt_l_channel, _, _ = cv2.split(gt_mask)

    assert gt_l_channel.size == exp_l_channel.size
    # add to total
    accuracy = np.sum(np.array(gt_l_channel) == np.array(exp_l_channel)) / float(gt_l_channel.size)
    cumulative_accuracy += accuracy


# report average accuracyerence

print 'Average RMSE'
print float(cumulative_rmse) / float(len(exp_grey_dict))
print 'Average accuracy in BW mask (%)'
print (float(cumulative_accuracy) / float(len(exp_bw_dict))) * 100
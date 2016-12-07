import os, sys, traceback
from glob import glob
import matplotlib.pyplot as plt
from os.path import join, basename, dirname
import matplotlib.image as mpimg
import numpy as np
# from scipy.misc import imread, imsave
import cv2

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir_data', default='.')

args = parser.parse_args()

# mask predictions
# dir_generated_masks = join(args.dir_data, 'images', 'mask_out')
dir_generated_masks = join(args.dir_data, 'images', 'greyscale_shadowmask')
# input
dir_shadow = join(args.dir_data, 'images', 'shadow')

# ground truth
dir_noshadow = join(args.dir_data, 'images', 'noshadow')

# output reconstructed image
dir_out = join(args.dir_data, 'images', 'recontruction')

prefix = './images/shadow'
# create albedo mask
for dir_scene in sorted(glob(join(dir_shadow, '*'))):
    for path_shadow in sorted(glob(join(dir_scene, '*.png'))):

        # read in input
        shadow = cv2.imread(path_shadow)
        cv2.imshow('original', shadow)

        #conver to lab
        shadow = cv2.cvtColor(shadow, cv2.COLOR_BGR2LAB)
        shadow_l_channel, shadow_a_channel, shadow_b_channel = cv2.split(shadow)        


        '''
        sanity check
        
        test = cv2.merge([shadow_l_channel, shadow_a_channel, shadow_b_channel])
        test = cv2.cvtColor(test, cv2.COLOR_LAB2BGR) 
        cv2.imshow('remerge', test)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''

        # get filename and scene
        f = None
        if path_shadow.startswith(dir_shadow):
            f = path_shadow[len(dir_shadow) + 1:]

        # path of ground truth
        path_noshadow = join(dir_noshadow, f)
        noshadow = cv2.imread(path_noshadow)
        noshadow = cv2.cvtColor(noshadow, cv2.COLOR_BGR2LAB)

        noshadow_l_channel, noshadow_a_channel, noshadow_b_channel = cv2.split(noshadow)

        # path of generated masks from CNN
        path_mask = join(dir_generated_masks, f)

        # read in l-channel
        shadow_mask = cv2.imread(path_mask)
        shadow_mask = cv2.cvtColor(shadow_mask, cv2.COLOR_BGR2LAB)
        mask_l_channel, mask_a_channel, mask_b_channel = cv2.split(shadow_mask)

        '''
        print 'shadow'
        print shadow_l_channel
        print 'mask'
        print mask_l_channel
        print 'noshadow'
        print noshadow_l_channel
        '''

        # result = mask_l_channel - shadow_l_channel
        # result = shadow_l_channel - mask_l_channel
        result = mask_l_channel + shadow_l_channel

        # print result
        '''
        cv2.imshow('shadow_mask', shadow_mask)
        cv2.imshow('shadow', shadow)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''

        # recompose
        result = cv2.merge([result, shadow_a_channel, shadow_b_channel])

        # convert result back to BGR
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

        # make the directory if not there
        dir_o = join(dir_out, basename(dir_scene))
        try: os.makedirs(dir_o)
        except: pass

        # output path
        path_result = join(dir_o, basename(path_shadow))

        print 'path_result ' + path_result

        cv2.imwrite(path_result, result)

        break

    # break

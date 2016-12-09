'''
Generate masks based on differences based on shadow and nonshadow ground truth
greyscale (gradient)
'''
import os, sys, traceback
from glob import glob
import matplotlib.pyplot as plt
from os.path import join, basename, dirname
import numpy as np
import cv2

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir_data', default='.')

args = parser.parse_args()

# inputs 
dir_shadow = join(args.dir_data, 'images', 'test_shadow')
# dir_noshadow = join(args.dir_data, 'images', 'noshadow')
# use the predicted
dir_noshadow = join(args.dir_data, 'images', 'test_predicted')

# outputs
dir_out = join(args.dir_data, 'images', 'greyscale_shadowmask')
dir_bw = join(args.dir_data, 'images', 'bw_shadowmask')


prefix = './images/shadow'
# create albedo mask
for dir_scene in sorted(glob(join(dir_shadow, '*'))):
    for path_shadow in sorted(glob(join(dir_scene, '*.png'))):

        shadow = cv2.imread(path_shadow)
        shadow = cv2.cvtColor(shadow, cv2.COLOR_BGR2LAB)
        shadow_l_channel, shadow_a_channel, shadow_b_channel = cv2.split(shadow)

        f = None
        if path_shadow.startswith(dir_shadow):
            f = path_shadow[len(dir_shadow) + 1:]

        path_noshadow = join(dir_noshadow, f)
        print path_noshadow
        
        #path_noshadow = join(path_noshadow, basename(path_shadow))
        noshadow = cv2.imread(path_noshadow)

        # sometimes we get rounding errors - reshape to fix them
        if noshadow.shape != shadow.shape:
            noshadow = cv2.resize(noshadow, (shadow.shape[1], shadow.shape[0])) 

        noshadow = cv2.cvtColor(noshadow, cv2.COLOR_BGR2LAB)
        noshadow_l_channel, noshadow_a_channel, noshadow_b_channel = cv2.split(noshadow)

        dir_o = join(dir_out, basename(dir_scene))
        try: os.makedirs(dir_o)
        except: pass

        # account for wraparound
        result = noshadow_l_channel - shadow_l_channel
        result[result > 230] = 0
        # result = cv2.merge([result, shadow_a_channel, shadow_b_channel])
        
        print 'path_shadow: ' + path_shadow
        print 'path_noshadow: ' + path_noshadow

        path_result = join(dir_o, basename(path_shadow))
        print 'path_result ' + path_result

        # imwrite uses BGR so convert first?
        # http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html
        # result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

        # write greyscale mask
        cv2.imwrite(path_result, result)

        # get directory of bw mask
        dir_o = join(dir_bw, basename(dir_scene))
        try: os.makedirs(dir_o)
        except: pass

        # path of bw mask
        path_bw = join(dir_o, basename(path_shadow))
        print 'path_bw: ' + path_bw

        result = noshadow_l_channel - shadow_l_channel

        # thresholding less than
        result[result < 50] = 0

        # everything else to white
        result[result > 0] = 255

        # result = cv2.merge([result, shadow_a_channel, shadow_b_channel])
        # result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

        # write bw mask
        cv2.imwrite(path_bw, result)
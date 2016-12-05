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

dir_shadow = join(args.dir_data, 'images', 'shadow')
dir_noshadow = join(args.dir_data, 'images', 'noshadow')
dir_out = join(args.dir_data, 'images', 'shadowmask')


prefix = './images/shadow'
# create albedo mask
for dir_scene in sorted(glob(join(dir_shadow, '*'))):
    for path_shadow in sorted(glob(join(dir_scene, '*.png'))):

#image2 = mpimg.imread(noshadow_path + path)
#image3 = image1 - image2

        shadow = cv2.imread(path_shadow)
        shadow = cv2.cvtColor(shadow, cv2.COLOR_BGR2LAB)
        shadow_l_channel, _, _ = cv2.split(shadow)
        # print shadow
        # mask = np.repeat((albedo.mean(2) != 0).astype(np.uint8)[..., np.newaxis] * 255, 3, 2)

        #f = os.path.join(path, filename)
        f = None
        if path_shadow.startswith(dir_shadow):
            f = path_shadow[len(dir_shadow) + 1:]

        path_noshadow = join(dir_noshadow, f)
        # print path_noshadow
        #path_noshadow = join(path_noshadow, basename(path_shadow))
        noshadow = cv2.imread(path_noshadow)
        noshadow = cv2.cvtColor(noshadow, cv2.COLOR_BGR2LAB)
        noshadow_l_channel, _, _ = cv2.split(noshadow)

        dir_o = join(dir_out, basename(dir_scene))
        try: os.makedirs(dir_o)
        except: pass

        result = noshadow_l_channel - shadow_l_channel
        # result = noshadow - shadow
        #result = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
        #result_l, _, _ = cv2.split(result)
        # cv2.imsave('shadow', shadow_l_channel)
        # cv2.imsave('noshadow', noshadow_l_channel)
        ''' 
        recover = shadow - result
        
        #for some reason the second one doesn't pass?
        try:
            assert recover.shape == noshadow.shape
            assert(shadow == noshadow + result).all()
        except AssertionError:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb) # Fixed format
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]

            print('An error occurred on line {} in statement {}'.format(line, text))
            exit(1)
        '''
        result[result > 230] = 0
        # print noshadow_l_channel
        # print shadow_l_channel
        # print result
        print 'path_shadow: ' + path_shadow
        print 'path_noshadow: ' + path_noshadow
        path_result = join(dir_o, basename(path_shadow))
        print 'path_result ' + path_result
    
        # result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # result = (255-gray_image)

        # assert np.array_equal(np.array(noshadow), np.array(shadow - result))
        cv2.imwrite(path_result, result)


        #imsave(path_result, result_l)
        #break

        '''
        plt.figure()
        plt.title('input - mask')
        plt.imshow(shadow - result)
        plt.show()
        '''

    # break
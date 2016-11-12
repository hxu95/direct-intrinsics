
# coding: utf-8


# In[2]:

# Set python path here
import sys
#manual path definition
sys.path.append('/home/hxu/caffe/python')
import matplotlib.pyplot as plt
import cv2
import numpy as np
import caffe
import direct_intrinsics as di


# In[3]:

# trained on sintel_scenes['train']
# modelfile = 'sintel_mit2_scale_1_2_v19_albedo_shading_epoch15000_lr0.002_do0.5_lambda1_iter_50000.caffemodel'
# trained on sintel_scenes['test']
modelfile = 'sintel_final_test.caffemodel'

# Load net
net = caffe.Net('direct_intrinsics.prototxt', modelfile, caffe.TEST)


# In[4]:

# Load an image
scene_id = 0
scene = di.sintel_scenes['train'][scene_id]
# scene = di.sintel_scenes['test'][scene_id]
print scene
#manual definition
img = cv2.imread('/home/hxu/data/sintel/images_mit_sintel/clean/{}/frame_0010.png'.format(scene))


# In[5]:

# Predict by Direct intrinsics CNN
a, s = di.predict(net, img)


# In[6]:

# Display results
plt.figure()
plt.title('input')
plt.imshow(di.bgr2rgb(img))
plt.figure()
plt.title('albedo')
plt.imshow(a)
plt.figure()
plt.title('shading')
plt.imshow(s)


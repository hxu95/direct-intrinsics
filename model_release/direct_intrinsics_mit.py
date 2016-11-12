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

# Load net
modelfile = 'mit_final_barron_train.caffemodel'
net = caffe.Net('direct_intrinsics.prototxt', modelfile, caffe.TEST)

# In[4]:

# Load an image
obj_id = 7
obj = di.mit_objects['test'][obj_id]
print obj
#manual definition
img = cv2.imread('/home/hxu/di-final/data/mit/MIT-intrinsic/data/{}/diffuse.png'.format(obj))
mask = cv2.imread('/home/hxu/di-final/data/mit/MIT-intrinsic/data/{}/mask.png'.format(obj))
#print img
#print mask
mask[mask > 0] = 1


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
plt.imshow(mask * a)
plt.figure()
plt.title('shading')
plt.imshow(mask * s)
plt.show()
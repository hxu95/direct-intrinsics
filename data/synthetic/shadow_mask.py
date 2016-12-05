#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import numpy as np
from scipy.misc import imread

image_path = 'images/'
shadow_path = image_path + 'shadow/'
noshadow_path = image_path + 'noshadow/'
shadowmask_path = image_path + 'shadowmask/'

path = 'blueprints/file0.png'

shadow = mpimg.imread(shadow_path + path)
noshadow = mpimg.imread(noshadow_path + path)
# shadowmask = shadow - noshadow
shadowmask = np.subtract(shadow, noshadow)
r = np.subtract(shadow, shadowmask)
#print r
#print noshadow
#assert(r == noshadow).all()

# Display results
plt.figure()
plt.title('input')
plt.imshow(shadow)
plt.figure()
plt.title('GT')
plt.imshow(noshadow)
plt.figure()
plt.title('mask')
plt.imshow(shadowmask)
plt.figure()
plt.title('input - mask')
plt.imshow(shadow - shadowmask)
plt.show()

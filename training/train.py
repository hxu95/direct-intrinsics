# coding: utf-8
# In[2]:

# Set python path here
import sys
sys.path.append('/home/hxu/di-final/modified_caffe/caffe/python')
sys.path.append('/home/hxu/caffe/python')
sys.path.append('/home/hxu/caffe_main/python')
import caffe

#solving
caffe.set_mode_cpu()
solver = caffe.get_solver('solver_without_shading.prototxt')
solver.solve()
import caffe

# Set pretrained model
caffe.set_mode_gpu()
modelfile = 'snapshot_no_shading_5000.caffemodel'

# Copy weights and solve
solver = caffe.get_solver('solver_without_mask.prototxt')
solver.net.copy_from(modelfile)
solver.solve()

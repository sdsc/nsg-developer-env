#!/usr/bin/env python3

import tensorflow as tf

print(tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))
print(tf.config.list_physical_devices('GPU'))
print(tf.test.is_built_with_cuda)
print(tf.test.gpu_device_name())

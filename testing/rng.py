import math
from numpy import random


bounding_box_size = (100, 100)
sample_size = 40
rng = random.default_rng()
x_mean = bounding_box_size[0] / 2
y_mean = bounding_box_size[1] / 2
x_sd = bounding_box_size[0] * 0.3
y_sd = bounding_box_size[1] * 0.3
x = rng.normal(x_mean, x_sd, sample_size)
y = rng.normal(y_mean, y_sd, sample_size)
x = sorted([math.floor(_) for _ in x])
y = sorted([math.floor(_) for _ in y])
print(x)
print(y)


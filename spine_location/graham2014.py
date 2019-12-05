from random import randint

import numpy as np
from matplotlib import pyplot as plt

SYN_NUM = 500
compartments = np.random.randint(50, 300, 200)
lmax = np.sum(compartments)

ys = []
xs = []
for i in range(SYN_NUM):
    l = 0
    r = randint(0, lmax)
    for c in compartments:
        l += c
        y = 0
        if l > r:
            y = (r - l + c)/c
            ys.append(y)
            xs.append(c)
            break

plt.scatter(xs, ys, alpha=0.5)
plt.show()
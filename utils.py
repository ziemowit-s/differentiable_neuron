import numpy as np


def alpha(x, param=1.0, div=1.0, add=0):
    if isinstance(x, (float, int)):
        xt = x
    else:
        xt = x.copy()

    xt = xt+add
    exp = np.exp(-xt/div)
    return param*(xt/(1-exp+1e-15))


def beta(x, param=1.0, div=1.0, add=0):
    return param*np.exp(-(x+add)/div)
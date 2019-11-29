import numpy as np
from hoc import HocObject
from neuron import h


def record(what, func=lambda seg: seg._ref_concentration):
    result = []
    for w in what:
        s = h.Vector().record(func(w))
        result.append(s)
    return result


def get_3d_concentration(species: list, time: HocObject):
    Z = []
    for s in species:
        Z.append(s.as_numpy())
    Z = np.array(Z)
    time = time.as_numpy()
    X, Y = np.meshgrid(time, range(0, len(species)))
    return X,Y,Z

import numpy as np
from neuron import h
from matplotlib import cm
from hoc import HocObject
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


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


def plot(species: list, time: HocObject):
    x, y, z = get_3d_concentration(species=species, time=time)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_title("Ca2+ diffusion with buffer. MOD-based.")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("compartment no.")
    ax.set_zlabel("Concentration (mM)")

    ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

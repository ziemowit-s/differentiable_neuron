from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.integrate import solve_ivp

STOP = 8.5  # ms
SLOPE = 1.1


def nf(t, y):
    return y*0.8


def plasticity(w, slope):
    if isinstance(w, list):
        w = np.array(w)
    return (2/(1+slope**-w))-1


def ltd(v, slope, threshold=-40):
    return 1/(1+slope**-(v-threshold))


def ltp(v, slope, threshold=0):
    return 1/(1+slope**-(v-threshold))


if __name__ == '__main__':
    x = np.arange(start=-70, stop=70, step=0.1)
    py = ltp(v=x, slope=SLOPE)
    dy = ltd(v=x, slope=SLOPE)

    z = []
    t = []
    for i, xi in enumerate(x):
        p = py[i]
        d = dy[i]
        y0 = (-d+2*p)/15
        sol = solve_ivp(nf, [0, STOP], y0=[y0], t_eval=np.arange(start=0, stop=STOP, step=0.1))
        t = sol.t
        z.append(sol.y[0])

    x, t = np.meshgrid(x, t)
    z = np.array(z).T

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x, t, plasticity(z, slope=SLOPE), cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_xlabel("mV")
    ax.set_ylabel("ms")
    ax.set_zlabel("plasticity")
    plt.show()

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.integrate import solve_ivp


def nf(t, y):
    return y


def plasticity(w, slope=1.3):
    if isinstance(w, list):
        w = np.array(w)
    return (2/(1+slope**-w))-1


def ltd(v, slope, threshold=-40):
    return 1/(1+slope**-(v-threshold))


def ltp(v, slope, threshold=0):
    return 1/(1+slope**-(v-threshold))


if __name__ == '__main__':
    STOP = 5
    x = np.arange(start=-70, stop=70, step=0.1)
    py = ltp(v=x, slope=1.3)
    dy = ltd(v=x, slope=1.3)

    z = []
    t = []
    for i, xi in enumerate(x):
        p = py[i]
        d = dy[i]
        y0 = (-d+2*p)/100
        sol = solve_ivp(nf, [0, STOP], y0=[y0], t_eval=np.arange(start=0, stop=STOP, step=0.1))
        t = sol.t
        z.append(sol.y[0])

    x, t = np.meshgrid(x, t)
    z = np.array(z).T

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x, t, plasticity(z), cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_xlabel("mV")
    ax.set_ylabel("ms")
    ax.set_zlabel("plasticity")
    plt.show()

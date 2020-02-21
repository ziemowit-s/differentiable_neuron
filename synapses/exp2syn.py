import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def nf(t, y):
    a = y[0]
    b = y[1]
    a = -a / tau1
    b = -b / tau2
    return np.array([a, b])


def get_factor(tau1, tau2):
    """
    Ensures peak conductance is 1
    """
    n = (tau1 * tau2)
    d = (tau2 - tau1)
    l = np.log(tau2 / tau1)
    tp = n/d * l

    tp1 = tp / tau1
    tp2 = tp / tau2

    e1 = np.exp(-tp1)
    e2 = np.exp(-tp2)

    factor = -e1 + e2
    return 1 / factor


def conductance(a, b):
    gs = []
    for a, b in zip(a, b):
        g = b - a
        gs.append(g)
    return np.array(gs)


STOP = 20
tau1 = 1
tau2 = 5


if __name__ == '__main__':
    w = 1
    factor = get_factor(tau1, tau2)
    print("factor", factor)

    a = w * factor
    b = w * factor
    
    sol = solve_ivp(nf, [0, STOP], y0=[a, b], t_eval=np.arange(start=0, stop=STOP, step=0.01))
    a = sol.y[0]
    b = sol.y[1]
    g = conductance(a, b)
    t = sol.t

    plt.plot(t, a, label='A', linewidth=1.0)
    plt.plot(t, b, label='B', linewidth=1.0)
    plt.plot(t, g, label='Conductance (B-A)', linewidth=2.0)
    plt.title('Exp2Syn with tau1=%s tau2=%s' % (tau1, tau2))
    plt.legend()
    plt.show()

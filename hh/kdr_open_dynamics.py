import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import utils


def nf(t, y=0):
    """
    The probability of open a gate.
    """
    n = y
    if n is None:
        n = 0
    return alpha * (1-n) - beta*n


def relu(x, param=1.0):
    x_temp = x.copy()
    x_temp[x_temp<0] = 0
    return param*x_temp


if __name__ == '__main__':
    x = np.arange(start=-120, stop=40, step=0.1)

    alpha_y = utils.alpha(x, param=0.01, div=10, add=55)
    beta_y = utils.beta(x, param=0.125, div=80, add=65)

    n_y5 = []
    for i, xi in enumerate(x):
        alpha = alpha_y[i]
        beta = beta_y[i]
        sol = solve_ivp(nf, [0, 5], y0=[0])
        n_y5.append(sol.y[0][-1])

    plt.plot(x, alpha_y, label='alpha (open)', linewidth=5.0)
    plt.plot(x, beta_y, label='beta (close)', linewidth=5.0)
    plt.plot(x, n_y5, label='KvDR open probability after 5 ms (for constant mV)', linewidth=5.0)
    plt.legend()
    plt.title('HH KvDR channel dynamics: dn/dt = alpha*(1-n) - beta*n')
    plt.show()

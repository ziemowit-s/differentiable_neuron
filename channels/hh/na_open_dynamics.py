import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import utils


def m(t, y=0):
    """
    The probability of open a gate.
    """
    return alpha_m * (1-y) - beta_m*y


def h(t, y=0):
    """
    The probability of open a gate.
    """
    return alpha_h * (1-y) - beta_h*y


if __name__ == '__main__':
    w = 2.0
    x = np.arange(start=-70, stop=20, step=0.1)

    alpha_my = utils.alpha(x, param=0.1, div=10, add=40)
    beta_my = utils.beta(x, param=4.0, div=18, add=65)

    alpha_hy = utils.beta(x, param=0.07, div=20, add=65)
    beta_hy = 1 / (utils.beta(x, param=1.0, div=10, add=35) + 1)

    open_na = []
    def op(t, y):
        return m(t, y) * h(t, y)
    for i, xi in enumerate(x):
        alpha_m = alpha_my[i]
        beta_m = beta_my[i]
        alpha_h = alpha_hy[i]
        beta_h = beta_hy[i]

        sol = solve_ivp(op, [0, 5], y0=[0])
        open_na.append(sol.y[0][-1])

    plt.plot(x, alpha_my, label='m alpha (open)', linewidth=w, color='blue')
    plt.plot(x, beta_my, label='m beta (close)', linewidth=w, color='green')
    plt.plot(x, alpha_hy, label='h alpha (open)', linewidth=w, color='orange')
    plt.plot(x, beta_hy, label='h beta (close)', linewidth=w, color='red')
    plt.plot(x, open_na, label='Na open probability', linewidth=w, color='black')
    plt.legend()
    plt.show()

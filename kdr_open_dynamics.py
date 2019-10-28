import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def alpha_kdr(x, param=1.0, div=1.0, add=0):
    xt = x.copy()
    xt = xt+add
    exp = np.exp(-xt/div)
    return param*(xt/(1-exp))


def beta_kdr(x, param=1.0, div=1.0, add=0):
    return param*np.exp(-(x+add)/div)


def n_inf(alpha, beta):
    return alpha/(alpha+beta)


def tau(alpha, beta):
    return 1/(alpha+beta)


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
    time = np.arange(start=0, stop=100, step=0.1)

    alpha_y = alpha_kdr(x, param=0.01, div=10, add=55)
    beta_y = beta_kdr(x, param=0.125, div=80, add=65)

    #n_y1 = []
    #for i, xi in enumerate(x):
    #    alpha = alpha_y[i]
    #    beta = beta_y[i]
    #    sol = solve_ivp(nf, [0, 1], y0=[0])
    #    n_y1.append(sol.y[0][-1])

    #n_y2 = []
    #for i, xi in enumerate(x):
    #    alpha = alpha_y[i]
    #    beta = beta_y[i]
    #    sol = solve_ivp(nf, [0, 2], y0=[0])
    #    n_y2.append(sol.y[0][-1])

    n_y5 = []
    for i, xi in enumerate(x):
        alpha = alpha_y[i]
        beta = beta_y[i]
        sol = solve_ivp(nf, [0, 5], y0=[0])
        n_y5.append(sol.y[0][-1])

    plt.plot(x, alpha_y, label='alpha', linewidth=5.0)
    plt.plot(x, beta_y, label='beta', linewidth=5.0)
    #plt.plot(x, n_y1, label='kv open probability after 1 ms')
    #plt.plot(x, n_y2, label='kv open probability after 2 ms')
    plt.plot(x, n_y5, label='KvDR open probability after 5 ms (for constant mV)', linewidth=5.0)
    plt.legend()
    plt.title('HH KvDR channel dynamics: dn/dt = alpha*(1-n) - beta*n')
    plt.show()

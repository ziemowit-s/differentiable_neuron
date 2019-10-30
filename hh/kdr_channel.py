import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

gk_bar = 0.036  # conductance bar (max conductance): S/cm^2
ek = -77  # equilibrium potential: mV


def alpha_nf(v):
    """
    alpha-param function
    :param v:
        voltage
    :return:
    """
    v = v+0.01
    #v = v+55

    exp = math.exp(-v)
    #exp = math.exp(-v/10)

    eq = v/(1-exp)

    return 0.01 * eq
    #return 0.01 * eq


def beta_nf(v):
    """
    beta-param function
    :param v:
        voltage
    :return:
    """
    v = v + 65
    exp = math.exp(-v/80)
    return 0.125 * exp


def nf(t, y=0):
    """
    The probability of open a gate.
    """
    n = y
    if n is None:
        n = 0
    a = alpha_nf(v)
    b = beta_nf(v)
    ab = (a+b)
    n_inf = a / ab
    tau = 1 / ab

    return (n_inf-n) / tau


if __name__ == '__main__':
    voltages = [-20, 0, 20, 30, 40, 45]

    for v in voltages:
        vol = v
        # for 10 ms membrane is depolarized to selected voltage v
        steps = 10  # ms
        step_size = 0.01
        t_eval = np.arange(start=0, stop=steps, step=step_size)
        sol = solve_ivp(nf, [0, steps], t_eval=t_eval, y0=[0])
        ns = sol.y.reshape(sol.y.shape[1])
        time = sol.t

        # then for 15 ms membrane is polarized to -70 mV
        v = -70  # mV
        steps = 15  # ms
        step_size = 0.01
        t_eval = np.arange(start=0, stop=steps, step=step_size)
        sol = solve_ivp(nf, [0, 100], t_eval=t_eval, y0=[ns[-1]])
        ns2 = sol.y.reshape(sol.y.shape[1])
        ns = np.concatenate([ns, ns2])
        time = np.concatenate([time, sol.t+time[-1]])

        i = gk_bar * ns * (v - ek)  # current
        gk = gk_bar * ns**4  # channel transduction


        #plt.plot(time, gk)
        plt.plot(time, i, label='%s mv' % vol)

    plt.legend()
    plt.xlabel('miliseconds')
    plt.ylabel('current (S/cm^2)')
    plt.show()
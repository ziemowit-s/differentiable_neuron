import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import utils


def m(t, y=0):
    a = utils.alpha(v, param=0.1, div=10, add=40)
    b = utils.beta(v, param=4.0, div=18, add=65)
    return a*(1-y) - b*y


def h(t, y=0):
    a = utils.beta(v, param=0.07, div=20, add=65)
    b = 1/(utils.beta(v, param=1.0, div=10, add=35)+1)
    return a*(1-y) - b*y


if __name__ == '__main__':
    gna_bar = 120  # conductance bar (max conductance): mS cm^-2
    ena = 50  # equilibrium potential: mV
    voltages = [-40, -30, -20, 20, 40]

    for v in voltages:
        v_temp = v
        v = -70  # mV
        # for 10 ms membrane is depolarized to selected voltage v
        steps = 1  # ms
        step_size = 0.01
        t_eval = np.arange(start=0, stop=steps, step=step_size)

        sol = solve_ivp(m, [0, steps], t_eval=t_eval, y0=[0])
        ms = sol.y.reshape(sol.y.shape[1])

        sol = solve_ivp(h, [0, steps], t_eval=t_eval, y0=[0])
        hs = sol.y.reshape(sol.y.shape[1])
        time = sol.t

        # then for 15 ms membrane is polarized to -70 mV
        v = v_temp  # mV
        steps = 10  # ms
        step_size = 0.01
        t_eval = np.arange(start=0, stop=steps, step=step_size)

        sol = solve_ivp(m, [0, 100], t_eval=t_eval, y0=[ms[-1]])
        ms = np.concatenate([ms, sol.y.reshape(sol.y.shape[1])])

        sol = solve_ivp(h, [0, 100], t_eval=t_eval, y0=[hs[-1]])
        hs = np.concatenate([hs, sol.y.reshape(sol.y.shape[1])])

        time = np.concatenate([time, sol.t+time[-1]])

        i = gna_bar * ms ** 3 * hs * (v - ena)  # current
        gk = gna_bar * ms ** 3 * hs  # channel transduction

        plt.plot(time, gk, label='%s mv' % v)
        #plt.plot(time, ms, label='open: %s mv' % v)
        #plt.plot(time, hs, label='inactive: %s mv' % v)
        #plt.plot(time, i)

    plt.legend()
    plt.xlabel('miliseconds')
    plt.ylabel('conductance')
    plt.show()
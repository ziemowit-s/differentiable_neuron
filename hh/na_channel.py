import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import utils

gna_bar = 0.012  # conductance bar (max conductance): S/cm^2
ena = 50  # equilibrium potential: mV


def m(t, y=0):
    a = utils.alpha(v, param=0.1, div=10, add=40)
    b = utils.beta(v, param=4.0, div=18, add=65)
    return a*(1-y) - b*y


def h(t, y=0):
    a = utils.beta(v, param=0.07, div=20, add=65)
    b = 1/(utils.beta(v, param=1.0, div=10, add=35)+1)
    return a*(1-y) - b*y


if __name__ == '__main__':
    voltages = [-40, -30, -20, 20, 40]

    for v in voltages:
        # then for 10 ms membrane is polarized to v_temp
        steps = 10  # ms
        step_size = 0.01
        t_eval = np.arange(start=0, stop=steps, step=step_size)

        sol = solve_ivp(m, [0, 100], t_eval=t_eval, y0=[0.0])  # 0.0 - fully close
        ms = sol.y.reshape(sol.y.shape[1])

        sol = solve_ivp(h, [0, 100], t_eval=t_eval, y0=[1.0])  # 1.0 - fully active
        hs = sol.y.reshape(sol.y.shape[1])

        time = sol.t

        i = gna_bar * ms ** 3 * hs * (v - ena)  # current
        gk = gna_bar * ms ** 3 * hs  # channel transduction

        #plt.plot(time, gk, label='%s mv' % v)
        #plt.plot(time, ms, label='open: %s mv' % v)
        #plt.plot(time, hs, label='inactive: %s mv' % v)

        # since out_of_cell is +; in_to_cell is -; so changed sign for chart
        plt.plot(time, -1*i, label='%s mv' % v)

    plt.legend()
    plt.xlabel('miliseconds')
    plt.ylabel('current (S/cm^2)')
    plt.show()
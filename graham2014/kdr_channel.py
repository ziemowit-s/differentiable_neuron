import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

gbar_kdr = 0.01  # S/cm^2
ek = -90  # mV
v_hn = 13  # mV
fi_n = -3
gamma_n = 0.7

T = 34  # st C
Q10 = 1
q = Q10**((T-24)/10)


def alpha(v):
    up = 96.48*fi_n*(v-v_hn)
    down = 8.315 * (273.16 + T)
    return np.exp((up/down))


def beta(v):
    up = 96.48*fi_n*gamma_n*(v-v_hn)
    down = 8.315 * (273.16 + T)
    return np.exp((up/down))


def tau(v):
    up = beta(v)
    down = 0.02 * q*(1+alpha(v))
    return np.max((up/down))


def n_inf(v):
    return 1/(1+alpha(v))


def n(t, y=0):
    return (n_inf(v)-y) / tau(v)


if __name__ == '__main__':
    voltages = [-20, 0, 20, 30, 40, 45]

    for v in voltages:
        vol = v
        # for 15 ms membrane is depolarized to selected voltage v
        steps = 15  # ms
        step_size = 0.01
        t_eval = np.arange(start=0, stop=steps, step=step_size)
        sol = solve_ivp(n, [0, steps], t_eval=t_eval, y0=[0])
        ns = sol.y.reshape(sol.y.shape[1])
        time = sol.t

        # then for 15 ms membrane is polarized to -70 mV
        v = -70  # mV
        steps = 15  # ms
        step_size = 0.01
        t_eval = np.arange(start=0, stop=steps, step=step_size)
        sol = solve_ivp(n, [0, 100], t_eval=t_eval, y0=[ns[-1]])
        ns2 = sol.y.reshape(sol.y.shape[1])

        # concat
        ns = np.concatenate([ns, ns2])
        time = np.concatenate([time, sol.t+time[-1]])

        i = gbar_kdr * ns * (v - ek)  # current
        gk = gbar_kdr * ns**4  # channel transduction


        #plt.plot(time, gk, label='%s mv' % vol)
        plt.plot(time, i, label='%s mv' % vol)

    plt.legend()
    plt.xlabel('miliseconds')
    plt.ylabel('current (S/cm^2)')
    plt.show()
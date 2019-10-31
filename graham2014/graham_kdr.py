import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from channel import Channel


class GrahamKdr(Channel):
    gbar_kdr = 0.01  # S/cm^2
    ek = -90  # mV
    v_hn = 13  # mV
    fi_n = -3
    gamma_n = 0.7

    T = 34  # st C
    Q10 = 1
    q = Q10 ** ((T - 24) / 10)

    def __init__(self):
        super().__init__()
        self.last_n = 0
        self.last_t = 0

    @staticmethod
    def alpha(v):
        up = 96.48 * GrahamKdr.fi_n * (v - GrahamKdr.v_hn)
        down = 8.315 * (273.16 + GrahamKdr.T)
        return np.exp((up / down))

    @staticmethod
    def beta(v):
        up = 96.48 * GrahamKdr.fi_n * GrahamKdr.gamma_n * (v - GrahamKdr.v_hn)
        down = 8.315 * (273.16 + GrahamKdr.T)
        return np.exp((up / down))

    @staticmethod
    def tau(v):
        up = GrahamKdr.beta(v)
        down = 0.02 * GrahamKdr.q * (1 + GrahamKdr.alpha(v))
        return np.max((up / down))

    @staticmethod
    def n_inf(v):
        return 1 / (1 + GrahamKdr.alpha(v))

    @staticmethod
    def n(t, y=0):
        return (GrahamKdr.n_inf(Channel.v) - y) / GrahamKdr.tau(Channel.v)

    def _compute(self, v, steps, step_size, t_eval):
        sol = solve_ivp(GrahamKdr.n, [0, steps], t_eval=t_eval, y0=[self.last_n])
        ns = sol.y.reshape(sol.y.shape[1])

        time = sol.t + self.last_t
        current = GrahamKdr.gbar_kdr * ns * (v - GrahamKdr.ek)  # current
        conductance = GrahamKdr.gbar_kdr * ns  # channel transduction

        self.last_n = ns[-1]
        self.last_t = time[-1]

        return time, current, conductance


if __name__ == '__main__':
    voltages = [-20, 0, 20, 30, 40, 45]

    for v in voltages:
        vol = v
        k_channel = GrahamKdr()
        k_channel.compute(v=v, steps=20)
        k_channel.compute(v=-70, steps=20)
        plt.plot(k_channel.get_time(), k_channel.get_conductance(), label='%s mv' % vol)
        #plt.plot(kdr.get_time(), kdr.get_current(), label='%s mv' % vol)

    plt.legend()
    plt.xlabel('miliseconds')
    plt.ylabel('current (S/cm^2)')
    plt.show()
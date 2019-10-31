import math
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import utils
from channel import Channel


class HHk(Channel):
    gk_bar = 0.036  # conductance bar (max conductance): S/cm^2
    ek = -77  # equilibrium potential: mV

    def __init__(self):
        super().__init__()
        self.last_n = 0
        self.t = 0

    @staticmethod
    def n(t, y=0):
        """
        The probability of open a gate.
        """
        n = y
        if n is None:
            n = 0
        #a = utils.alpha(Channel.v, param=0.01, div=10, add=55)  # HH original params
        a = utils.alpha(Channel.v, param=0.01, div=1, add=0.01)
        b = utils.beta(Channel.v, param=0.125, div=80, add=65)
        ab = (a+b)
        n_inf = a / ab
        tau = 1 / ab

        return (n_inf-n) / tau

    def _compute(self, v, steps, step_size, t_eval):
        sol = solve_ivp(HHk.n, [0, steps], t_eval=t_eval, y0=[self.last_n])
        ns = sol.y.reshape(sol.y.shape[1])

        time = sol.t + self.t
        current = HHk.gk_bar * ns * (v - HHk.ek)  # current
        conductance = HHk.gk_bar * ns ** 4  # channel transduction

        self.last_n = ns[-1]
        self.t = time[-1]

        return time, current, conductance


if __name__ == '__main__':
    voltages = [-20, 0, 20, 30, 40, 45]

    for v in voltages:
        vol = v
        k_channel = HHk()
        k_channel.compute(v=v, steps=20)
        k_channel.compute(v=-70, steps=20)
        #plt.plot(kdr.times, kdr.currents, label='%s mv' % vol)
        plt.plot(k_channel.get_time(), k_channel.get_conductance(), label='%s mv' % vol)

    plt.legend()
    plt.xlabel('ms')
    plt.ylabel('conductancy (S/cm^2)')
    plt.show()
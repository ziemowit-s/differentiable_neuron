import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import utils
from channel import Channel


class HHna(Channel):
    gna_bar = 0.012  # conductance bar (max conductance): S/cm^2
    ena = 50  # equilibrium potential: mV

    def __init__(self):
        super().__init__()
        self.last_m = 0.0  # fully closed channel
        self.last_h = 1.0  # fully active channel
        self.last_t = 0

    @staticmethod
    def d_m(t, y=0):
        a = utils.alpha(Channel.v, param=0.1, div=10, add=40)
        b = utils.beta(Channel.v, param=4.0, div=18, add=65)
        return a * (1 - y) - b * y

    @staticmethod
    def d_h(t, y=0):
        a = utils.beta(Channel.v, param=0.07, div=20, add=65)
        b = 1 / (utils.beta(Channel.v, param=1.0, div=10, add=35) + 1)
        return a * (1 - y) - b * y

    def _compute(self, v, steps, step_size, t_eval):
        sol = solve_ivp(HHna.d_m, [0, 100], t_eval=t_eval, y0=[self.last_m])
        ms = sol.y.reshape(sol.y.shape[1])

        sol = solve_ivp(HHna.d_h, [0, 100], t_eval=t_eval, y0=[self.last_h])
        hs = sol.y.reshape(sol.y.shape[1])

        time = sol.t + self.last_t
        conductance = HHna.gna_bar * ms ** 3 * hs  # channel transduction
        current = conductance * (v - HHna.ena)  # current

        self.last_m = ms[-1]
        self.last_h = hs[-1]
        self.last_t = time[-1]

        return time, current, conductance


if __name__ == '__main__':
    voltages = [-40, -30, -20, 20, 40]

    for v in voltages:
        na_channel = HHna()
        na_channel.compute(v=v, steps=10)
        # since out_of_cell is +; in_to_cell is -; so changed sign for chart
        plt.plot(na_channel.get_time(), -1 * na_channel.get_current(), label='%s mv' % v)

    plt.legend()
    plt.xlabel('ms')
    plt.ylabel('current (S/cm^2)')
    plt.show()
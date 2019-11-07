import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import numpy as np
from channel import Channel


class GrahamCar(Channel):
    g_bar = 0.03  # conductance bar (max conductance): S/cm^2
    eq = 10  # equilibrium potential: mV
    v_hm = -30  # mv
    v_hh = -65  # mV
    k_m = -6.7
    k_h = 11.8
    tau_m = 3.6  # mS
    tau_h = 20  # mS

    m_inf = None
    h_inf = None

    def __init__(self):
        super().__init__()
        self.last_m = 0.0  # fully closed channel
        self.last_h = 0.0  # fully active channel
        self.last_t = 0

    @staticmethod
    def _m_inf(v):
        exp = np.exp(-(v-GrahamCar.v_hm) / GrahamCar.k_m)
        return 1 / (1 + exp)

    @staticmethod
    def _h_inf(v):
        exp = np.exp(-(v - GrahamCar.v_hh) / GrahamCar.k_h)
        return 1 / (1 + exp)

    @staticmethod
    def m(t, y=0):
        return (GrahamCar.m_inf - y) / GrahamCar.tau_m

    @staticmethod
    def h(t, y=0):
        return (GrahamCar.h_inf - y) / GrahamCar.tau_h

    def _compute(self, v, steps, step_size, t_eval):
        GrahamCar.m_inf = self._m_inf(v)
        GrahamCar.h_inf = self._h_inf(v)

        sol = solve_ivp(GrahamCar.m, [0, steps], t_eval=t_eval, y0=[self.last_m])
        ms = sol.y.reshape(sol.y.shape[1])

        sol = solve_ivp(GrahamCar.h, [0, steps], t_eval=t_eval, y0=[self.last_h])
        hs = sol.y.reshape(sol.y.shape[1])

        time = sol.t + self.last_t
        conductance = GrahamCar.g_bar * ms ** 3 * hs
        current = conductance * (v - GrahamCar.eq)

        self.last_m = ms[-1]
        self.last_h = hs[-1]
        self.last_t = time[-1]

        return time, current, conductance


if __name__ == '__main__':
    voltages_for_plot = [-70, -40, -20, 0, 20, 30, 40, 45]
    voltages = np.arange(start=-100, stop=100, step=1)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Graham 2014 Kdr')

    m_infs = []
    h_infs = []
    for v in voltages:
        vol = v
        k_channel = GrahamCar()
        k_channel.compute(v=v, steps=100)
        m_infs.append(k_channel.m_inf)
        h_infs.append(k_channel.h_inf)

        if v in voltages_for_plot:
            k_channel.compute(v=-70, steps=100)
            ax1.plot(k_channel.get_time(), k_channel.get_conductance(), label='%s mv' % vol)
    ax1.set_title('channel conductance')
    ax1.legend()
    ax1.set(xlabel='ms', ylabel='current (S/cm^2)')

    ax2.set_title('infs')
    ax2.set(xlabel='mV')
    ax2.plot(voltages, m_infs, label='m_inf')
    ax2.set(xlabel='mV')
    ax2.plot(voltages, h_infs, label='h_inf')
    ax2.legend()

    plt.show()
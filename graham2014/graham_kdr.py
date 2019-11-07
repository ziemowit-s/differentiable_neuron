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

    n_inf = None
    tau = None

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
    def _tau(v):
        """
        in ms
        :param v:
        :return:
        """
        up = GrahamKdr.beta(v)
        down = 0.02 * GrahamKdr.q * (1 + GrahamKdr.alpha(v))
        return np.max([(up / down), 2])

    @staticmethod
    def _n_inf(v):
        return 1 / (1 + GrahamKdr.alpha(v))

    @staticmethod
    def d_n(t, y=0):
        return (GrahamKdr.n_inf - y) / GrahamKdr.tau

    def _compute(self, v, steps, step_size, t_eval):
        GrahamKdr.n_inf = self._n_inf(v)
        GrahamKdr.tau = self._tau(v)
        sol = solve_ivp(GrahamKdr.d_n, [0, steps], t_eval=t_eval, y0=[self.last_n])
        ns = sol.y.reshape(sol.y.shape[1])

        time = sol.t + self.last_t
        current = GrahamKdr.gbar_kdr * ns * (v - GrahamKdr.ek)  # current
        conductance = GrahamKdr.gbar_kdr * ns  # channel transduction

        self.last_n = ns[-1]
        self.last_t = time[-1]

        return time, current, conductance


if __name__ == '__main__':
    voltages_for_plot = [-20, 0, 20, 30, 40, 45]
    voltages = np.arange(start=-70, stop=60, step=1)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.suptitle('Graham 2014 Kdr')

    n_infs = []
    taus = []
    for v in voltages:
        vol = v
        k_channel = GrahamKdr()
        k_channel.compute(v=v, steps=20)
        n_infs.append(k_channel.n_inf)
        taus.append(k_channel.tau)

        if v in voltages_for_plot:
            k_channel.compute(v=-70, steps=20)
            ax1.plot(k_channel.get_time(), k_channel.get_conductance(), label='%s mv' % vol)
    ax1.set_title('channel conductance')
    ax1.legend()
    ax1.set(xlabel='ms', ylabel='current (S/cm^2)')

    ax2.set_title('n_inf')
    ax2.set(xlabel='mV')
    ax2.plot(voltages, n_infs)

    ax3.set_title('tau')
    ax3.set(xlabel='mV')
    ax3.plot(voltages, taus)

    plt.show()
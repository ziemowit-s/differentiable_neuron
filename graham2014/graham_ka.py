import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from channel import Channel


class GrahamKa(Channel):
    gbar_ka_star = 0.03  # S/cm^2
    x = None

    @staticmethod
    def gbar_ka(x):
        if x < 350:
            return GrahamKa.gbar_ka_star * (1+x)/100
        else:
            return GrahamKa.gbar_ka_star * 4.5/100

    ek = -90  # mV
    v_hl = -56  # mV
    fi_l = 3

    # Proxim < 100 um
    fi_n_proxim = -1.5
    v_hn_proxim = 11  # mV
    gamma_n_proxim = 0.55
    a0_proxim = 0.05

    # Distal > 100 um
    fi_n_distal = -1.8
    v_hn_distal = -1  # mV
    gamma_n_distal = 0.39
    a0_distal = 0.1


    T = 34  # st C
    Q10 = 5
    q = Q10 ** ((T - 24) / 10)

    def __init__(self, x):
        super().__init__()
        self.x = x
        self.last_n = 0
        self.last_l = 0
        self.last_t = 0

    @staticmethod
    def alpha_n(v, x):
        up = 96.48 * GrahamKa.fi(x) * (v - GrahamKa.v_hn(x))
        down = 8.315 * (273.16 + GrahamKa.T)
        return np.exp((up / down))

    @staticmethod
    def alpha_l(v, x):
        up = 96.48 * GrahamKa.fi_l * (v - GrahamKa.v_hn(x))
        down = 8.315 * (273.16 + GrahamKa.T)
        return np.exp((up / down))

    @staticmethod
    def beta(v, x):
        up = 96.48 * GrahamKa.fi(x) * GrahamKa.gamma_n(x) * (v - GrahamKa.v_hn(x))
        down = 8.315 * (273.16 + GrahamKa.T)
        return np.exp((up / down))

    @staticmethod
    def fi(x):
        fi_n = GrahamKa.fi_n_proxim if x < 100 else GrahamKa.fi_n_distal
        return fi_n - 1/(1 + np.exp(((v+40)/5)))

    @staticmethod
    def v_hn(x):
        return GrahamKa.v_hn_proxim if x < 100 else GrahamKa.v_hn_distal

    @staticmethod
    def gamma_n(x):
        return GrahamKa.gamma_n_proxim if x < 100 else GrahamKa.gamma_n_distal

    @staticmethod
    def a0(x):
        return GrahamKa.a0_proxim if x < 100 else GrahamKa.a0_distal

    @staticmethod
    def tau_n_func(v, x):
        """
        in ms
        :param v:
        :param x:
        :return:
        """
        up = GrahamKa.beta(v, x)
        down = GrahamKa.a0(x) * GrahamKa.q * (1 + GrahamKa.alpha_n(v, x))
        return np.max([(up / down), 0.1])

    @staticmethod
    def tau_l_func(v):
        """
        in ms
        :param v:
        :param x:
        :return:
        """
        return np.max([0.26*(v+50), 2])

    @staticmethod
    def n_inf_func(v, x):
        return 1 / (1 + GrahamKa.alpha_n(v, x))

    @staticmethod
    def l_inf(v, x):
        return 1/(1+GrahamKa.alpha_l(v, x))

    @staticmethod
    def n(t, y=0):
        return (GrahamKa.n_inf_func(Channel.v, GrahamKa.x) - y) / GrahamKa.tau_n_func(Channel.v, GrahamKa.x)

    @staticmethod
    def l(t, y=0):
        return (GrahamKa.l_inf(Channel.v, GrahamKa.x) - y) / GrahamKa.tau_l_func(Channel.v)

    def _compute(self, v, steps, step_size, t_eval):
        GrahamKa.x = self.x
        sol = solve_ivp(GrahamKa.n, [0, steps], t_eval=t_eval, y0=[self.last_n])
        ns = sol.y.reshape(sol.y.shape[1])

        sol = solve_ivp(GrahamKa.l, [0, steps], t_eval=t_eval, y0=[self.last_l])
        ls = sol.y.reshape(sol.y.shape[1])

        time = sol.t + self.last_t
        conductance = GrahamKa.gbar_ka(GrahamKa.x) * ns * ls  # channel transduction
        current = conductance * (v - GrahamKa.ek)  # current

        self.last_n = ns[-1]
        self.last_l = ls[-1]
        self.last_t = time[-1]

        return time, current, conductance


if __name__ == '__main__':
    voltages = [-20, 0, 20, 30, 40, 45]
    x = 150  # um from soma

    for v in voltages:
        vol = v
        k_channel = GrahamKa(x=x)
        k_channel.compute(v=v, steps=20)
        k_channel.compute(v=-70, steps=20)
        plt.plot(k_channel.get_time(), k_channel.get_conductance(), label='%s mv' % vol)
        #plt.plot(k_channel.get_time(), k_channel.get_current(), label='%s mv' % vol)

    plt.legend()
    plt.xlabel('ms')
    plt.ylabel('current (S/cm^2)')
    plt.show()
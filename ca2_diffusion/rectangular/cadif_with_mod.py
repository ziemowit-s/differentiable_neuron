import numpy as np
from neuron import h, gui
import matplotlib.pyplot as plt
from neuron.units import mV, ms, mM, uM
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import cm

from ca2_diffusion.rectangular.utils import record, get_3d_concentration


class Cell:
    def __init__(self, name):
        """
        spine_head->spine_neck->dendrite
        """
        self._name = name

        self.head = h.Section(name='head', cell=self)
        self.head.L = 0.5
        self.head.diam = 0.5
        self.head.nseg = 11

        self.neck = h.Section(name='neck', cell=self)
        self.neck.L = 0.5
        self.neck.diam = 0.1
        self.neck.nseg = 11

        self.dend = h.Section(name='dend', cell=self)
        self.dend.L = 11
        self.dend.diam = 1.0
        self.dend.nseg = 110

        self.head.insert('cadifusrect')
        self.neck.insert('cadifusrect')

        self.all = [self.dend, self.neck, self.head]

        self.head.connect(self.neck)
        self.neck.connect(self.dend(0.5))

    def __repr__(self):
        return "Cell[{}]".format(self._name)


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    cell = Cell(name=0)
    h.cvode.active(1)

    # record
    cas = record(what=cell.head, func=lambda seg: seg.cadifusrect._ref_ca[0])
    t = h.Vector().record(h._ref_t)

    # init
    h.finitialize(-65 * mV)
    cell.head(0.5).ca_cadifusrect[0] = 0.01
    h.cvode.re_init()

    # run
    h.continuerun(0.05 * ms)
    x, y, z = get_3d_concentration(species=cas, time=t)

    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_title("Ca2+ diffusion with buffer. MOD-based.")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("compartment no.")
    ax.set_zlabel("Concentration (mM)")

    ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()

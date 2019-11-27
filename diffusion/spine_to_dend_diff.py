import numpy as np
from neuron import h, gui
import matplotlib.pyplot as plt
from neuron.units import mV, ms, mM, uM
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import cm


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
        self.neck.diam = 0.5
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

    # record
    cas = []
    for seg in cell.head:
        ca = h.Vector().record(seg.cadifusrect._ref_ca[0])
        cas.append(ca)
    t = h.Vector().record(h._ref_t)

    # init
    h.finitialize(-70 * mV)
    cell.head(0.5).ca_cadifusrect[0] = 0.01
    h.cvode.re_init()

    # run
    h.continuerun(0.5 * ms)

    # plot
    Z = []
    for ca in cas:
        Z.append(ca.as_numpy())
    Z = np.array(Z)
    t = t.as_numpy()
    X, Y = np.meshgrid(t, range(0, len(cas)))

    plt.gca(projection='3d').plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()




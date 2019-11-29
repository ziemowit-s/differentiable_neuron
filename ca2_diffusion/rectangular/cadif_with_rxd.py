from matplotlib import cm
from neuron import h
from neuron.units import mV, ms
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

from ca2_diffusion.rectangular.cell_rxd import CellRxD
from ca2_diffusion.rectangular.utils import record, get_3d_concentration

if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)

    cell = CellRxD(name=0)

    # record
    cas = record(cell.ca.nodes)
    t = h.Vector().record(h._ref_t)

    # init
    h.finitialize(-65*mV)
    cell.ca.nodes[5].concentration = 0.01
    h.cvode.re_init()

    # run
    h.continuerun(0.05 * ms)
    x, y, z = get_3d_concentration(species=cas, time=t)

    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_title("Ca2+ diffusion with buffer. RxD-based.")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("compartment no.")
    ax.set_zlabel("Concentration (mM)")

    ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()



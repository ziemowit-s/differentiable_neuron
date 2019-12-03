from neuron import h
import matplotlib.pyplot as plt
from neuron.units import mV, ms

from ca2_diffusion.rectangular.cells.cell_rxd_ca import CellRxDCa
from ca2_diffusion.rectangular.utils import record, plot3D


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)

    cell = CellRxDCa(name="cell")
    cell.add_sec(name="head", diam=1, l=1, nseg=11)
    cell.add_rxd()

    # record
    cas_head = record(cell.ca.nodes)
    t = h.Vector().record(h._ref_t)

    # init
    h.finitialize(-65*mV)
    cell.ca.nodes[5].concentration = 0.01
    h.cvode.re_init()

    # run
    h.continuerun(0.05 * ms)

    plot3D(specie=cas_head, time=t)
    plt.show()



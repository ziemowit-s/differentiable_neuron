from neuron import h
import matplotlib.pyplot as plt
from neuron.units import mV, ms

from ca2_diffusion.rectangular.cell_rxd import CellRxD
from ca2_diffusion.rectangular.utils import record,  plot

if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)

    cell = CellRxD(name=0)

    # record
    cas_head = record(cell.ca.nodes)
    t = h.Vector().record(h._ref_t)

    # init
    h.finitialize(-65*mV)
    cell.ca.nodes[5].concentration = 0.01
    h.cvode.re_init()

    # run
    h.continuerun(0.05 * ms)

    plot(species=cas_head, time=t)
    plt.show()



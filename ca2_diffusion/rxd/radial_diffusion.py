from neuron import h, gui
from neuron.units import mV, ms
import matplotlib.pyplot as plt

from ca2_diffusion.rectangular.cells.cell_rxd_ca import CellRxDCa

if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)

    cell = CellRxDCa(name="cell")
    cell.add_sec(name="head", diam=1, l=1, nseg=11)
    cell.add_sec(name="neck", diam=0.5, l=0.5, nseg=11)
    cell.connect(fr='neck', to='head')
    cell.add_rxd()

    # init
    h.finitialize(-65*mV)
    cell.ca[cell.regs['head']].nodes[0].concentration = 0.5
    h.cvode.re_init()

    # plot shape

    ps = h.PlotShape(True)
    ps.variable('cai')
    ps.scale(0, 0.01)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')

    # run
    #h.continuerun(5 * ms)



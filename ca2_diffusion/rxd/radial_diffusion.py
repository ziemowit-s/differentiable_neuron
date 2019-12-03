from neuron import h, rxd, gui
from neuron.units import mV, ms
import matplotlib.pyplot as plt

from ca2_diffusion.rectangular.cells.cell_rxd import CellRxD


def add_rxd(sec):
    region = rxd.Region(secs=sec, nrn_region='i')

    ca = rxd.Species(regions=region, initial=50e-6, name='ca', charge=2, d=0.6)
    cabuf = rxd.Species(regions=region, initial=0.003, name='cabuf', charge=0)
    ca_cabuf = rxd.Species(regions=region, initial=0, name='ca_cabuf', charge=0)

    reaction = rxd.Reaction(ca + cabuf, ca_cabuf, 100, 0.1)

    return region, [ca, ca_cabuf, cabuf], reaction


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)

    cell = CellRxD(name="cell", add_rxd_func=add_rxd)
    cell.add(name="head", diam=1, l=1, nseg=11)

    # init
    h.finitialize(-65*mV)
    cell.species['ca'].nodes[5].concentration = 0.01
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



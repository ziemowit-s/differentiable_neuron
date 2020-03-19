from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
from neuron.units import mV, ms

from diffusion.ca2.rectangular.cells.cell import Cell
from diffusion.ca2.rectangular.utils import record, plot3D_specie

if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    cell = Cell(name=0, mechanism='cadifusrect')
    cell.add_sec(name="head", diam=1, l=1, nseg=11)
    h.cvode.active(1)

    head = cell.secs['head']

    # record
    cas_head = record(what=head, func=lambda seg: seg.cadifusrect._ref_ca[0])
    t = h.Vector().record(h._ref_t)

    # init
    h.finitialize(-65 * mV)
    head(0.5).ca_cadifusrect[0] = 0.02
    h.cvode.re_init()

    # run
    h.continuerun(0.1 * ms)

    data = []
    for i in np.arange(start=0, stop=1 + 1e-10, step=1 / head.nseg):
        data.append(list(head(i).ca_cadifusrect))
    data = np.array(data)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data)

    plot3D_specie(specie=cas_head, time=t)

    plt.show()

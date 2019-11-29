from neuron import h
import matplotlib.pyplot as plt
from neuron.units import mV, ms

from ca2_diffusion.rectangular.cell import Cell
from ca2_diffusion.rectangular.utils import record, plot

if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    cell = Cell(name=0, mechanism='cadifusrect')
    h.cvode.active(1)

    # record
    cas_head = record(what=cell.head, func=lambda seg: seg.cadifusrect._ref_ca[0])
    cas_neck = record(what=cell.neck, func=lambda seg: seg.cadifusrect._ref_ca[0])
    cas_dend = record(what=cell.dend, func=lambda seg: seg.cadifusrect._ref_ca[0])
    t = h.Vector().record(h._ref_t)

    # init
    h.finitialize(-65 * mV)
    cell.head(0.5).ca_cadifusrect[0] = 0.01
    h.cvode.re_init()

    # run
    h.continuerun(5 * ms)

    plot(species=cas_head, time=t)
    plot(species=cas_neck, time=t)
    plot(species=cas_dend, time=t)
    plt.show()


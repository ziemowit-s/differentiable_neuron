import numpy as np
from neuron import h, gui
from neuron.units import mV, ms
import matplotlib.pyplot as plt
import time

from ca2_diffusion.rectangular.cells.cell_rxd_ca import CellRxDCa


RUNTIME = 5 * ms
STEPSIZE = 0.005 * ms
DELAY = 20 * ms  # between steps

if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)

    cell = CellRxDCa(name="cell")
    cell.add_sec(name="head", diam=1, l=1, nseg=40)
    cell.add_sec(name="neck", diam=0.5, l=0.5, nseg=40)
    cell.add_sec(name="dend", diam=0.5, l=5, nseg=200)
    cell.connect(fr='head', to='neck')
    cell.connect(fr='neck', to='dend', to_loc=0.5)
    cell.add_rxd()

    # init
    h.finitialize(-65*mV)
    #TODO how to check if mM concentration diffuse rapidly or there is a "wall" on dendrite
    head_last = cell.secs['head'].nseg+cell.secs['neck'].nseg+cell.secs['dend'].nseg - 1
    cell.ca.nodes[head_last].concentration = 0.5
    h.cvode.re_init()

    # plot shape
    ps = h.PlotShape(True)
    ps.variable('cai')
    ps.scale(0, 0.01)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')
    #h.PlotShape(False).plot(plt)

    # run
    sleep = 3
    print("sleep before run for: %s seconds", sleep)
    time.sleep(sleep)
    before = time.time()
    const_delay = DELAY / 1000  # in seconds
    for i in np.arange(0, RUNTIME, STEPSIZE):
        h.continuerun(i * ms)
        current = time.time()
        comp_time_ms = current - before

        delay = const_delay - comp_time_ms
        if delay < 0:
            delay = 0

        time.sleep(delay)
        before = time.time()
        ps.fastflush()
        print(i, "ms", 'comp_time_ms:', round(comp_time_ms*1000, 0), 'delay:', round(delay*1000, 0))


from neuron import h, rxd, gui
from neuron.units import mV, ms
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')
h.cvode.atol(1e-8)
h.cvode.active(1)

head = h.Section(name='head')
head.L = 1
head.diam = 1
head.nseg = 11
neck = h.Section(name='neck')
neck.L = 0.5
neck.diam = 0.5
neck.nseg = 11
head.connect(neck)

cyt_head = rxd.Region(secs=head, nrn_region='i')
cyt_neck = rxd.Region(secs=neck, nrn_region='i')

ca = rxd.Species(regions=[cyt_head, cyt_neck], initial=50e-6, name='ca', charge=2, d=0.6)
cabuf = rxd.Species(regions=[cyt_head, cyt_neck], initial=0.003, name='cabuf', charge=0)

ca_cabuf = rxd.Species(regions=[cyt_head, cyt_neck], initial=0, name='ca_cabuf', charge=0)
reaction = rxd.Reaction(ca + cabuf, ca_cabuf, 100, 0.1)

# init
h.finitialize(-65 * mV)
ca[cyt_head].nodes[10].concentration = 0.01
h.cvode.re_init()

# plot shape

ps = h.PlotShape(True)
ps.variable('cai')
ps.scale(0, 0.01)
ps.show(0)
ps.exec_menu('Shape Plot')
#ps.plot(plt)

# run
h.continuerun(5 * ms)



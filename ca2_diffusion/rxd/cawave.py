from neuron import h, rxd
from matplotlib import pyplot as plt

h.load_file('stdrun.hoc')

gip3r = 12040
gserca = 0.3913
gleak = 6.020
kserca = 0.1
kip3 = 0.15
kact = 0.4

sec = h.Section(name='sec')
sec.L = 101
sec.diam = 1
# By chunking the neuron into a large number of segments
# we increase the resolution of the output at the expense of processing power.
sec.nseg = 101

# Where
cyt = rxd.Region(h.allsec(), nrn_region='i', geometry=rxd.FractionalVolume(0.8, surface_fraction=1))
er = rxd.Region(h.allsec(), geometry=rxd.FractionalVolume(0.2))
cyt_er_membrane = rxd.Region(h.allsec(), geometry=rxd.DistributedBoundary(1))

# What
ca = rxd.Species(regions=[cyt, er], d=0.08, name='ca', charge=2, initial=1e-4, atolscale=1e-6)
ip3 = rxd.Species(regions=cyt, d=1.41, initial=0.1)

# ??
ip3r_gate_stage = rxd.State(cyt_er_membrane, initial=0.8)
h_gate = ip3r_gate_stage[cyt_er_membrane]

# How
serca = rxd.MultiCompartmentReaction(ca[cyt], ca[er],
                                     gserca / ((kserca / (1000. * ca[cyt])) ** 2 + 1),
                                     membrane=cyt_er_membrane,
                                     custom_dynamics=True)
leak = rxd.MultiCompartmentReaction(ca[er], ca[cyt], gleak, gleak, membrane=cyt_er_membrane)



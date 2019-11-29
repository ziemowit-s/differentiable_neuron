import numpy as np
from matplotlib import cm
from neuron import h, rxd
from neuron.units import mV, ms
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

from ca2_diffusion.rectangular.utils import record, get_3d_concentration

h.load_file('stdrun.hoc')
h.cvode.atol(1e-8)
h.cvode.active(1)

head = h.Section(name='head')
head.L = 1
head.diam = 1
head.nseg = 11

cyt = rxd.Region(secs=head, nrn_region='i')

ca = rxd.Species(regions=cyt, initial=50e-6, name='ca', charge=2, d=0.6)
cabuf = rxd.Species(regions=cyt, initial=0.003, name='cabuf', charge=0)

ca_cabuf = rxd.Species(regions=cyt, initial=0, name='ca_cabuf', charge=0)
reaction = rxd.Reaction(ca + cabuf, ca_cabuf, 100, 0.1)

# record
cas = record(ca.nodes)
t = h.Vector().record(h._ref_t)

# init
h.finitialize(-65*mV)
ca.nodes[5].concentration = 0.01
h.cvode.re_init()

# run
h.continuerun(0.05 * ms)
x, y, z = get_3d_concentration(species=cas, time=t)

# plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_title("Ca2+ diffusion with buffer. RxD-based.")
ax.set_xlabel("compartment no.")
ax.set_ylabel("Time (ms)")
ax.set_zlabel("Concentration (mM)")

ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
plt.show()



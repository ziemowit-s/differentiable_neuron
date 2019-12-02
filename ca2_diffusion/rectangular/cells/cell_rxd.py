from neuron import rxd
from ca2_diffusion.rectangular.cells.cell import Cell


class CellRxD(Cell):
    def __init__(self, name):
        super().__init__(name)

        self.cyt = rxd.Region(secs=self.head, nrn_region='i')

        self.ca = rxd.Species(regions=self.cyt, initial=50e-6, name='ca', charge=2, d=0.6)
        self.cabuf = rxd.Species(regions=self.cyt, initial=0.003, name='cabuf', charge=0)

        self.ca_cabuf = rxd.Species(regions=self.cyt, initial=0, name='ca_cabuf', charge=0)
        self.reaction = rxd.Reaction(self.ca + self.cabuf, self.ca_cabuf, 100, 0.1)

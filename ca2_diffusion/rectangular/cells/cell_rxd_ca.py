from neuron import rxd

from ca2_diffusion.rectangular.cells.cell_rxd import CellRxD


class CellRxDCa(CellRxD):
    def _add_rxd(self, regs: dict):
        """
        Must be called after all secs are set.
        """
        regs = regs.values()
        self.ca = rxd.Species(regions=regs, initial=50e-6, name='ca', charge=2, d=0.6)
        self.cabuf = rxd.Species(regions=regs, initial=0.003, name='cabuf', charge=0)

        self.ca_cabuf = rxd.Species(regions=regs, initial=0, name='ca_cabuf', charge=0)
        self.reaction = rxd.Reaction(self.ca + self.cabuf, self.ca_cabuf, 100, 0.1)

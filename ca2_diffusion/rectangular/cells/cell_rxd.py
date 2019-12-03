import abc
from ca2_diffusion.rectangular.cells.cell import Cell


class CellRxD(Cell):
    def __init__(self, name, add_rxd_func=None):
        super().__init__(name)
        self._rxd_func = add_rxd_func
        self.regions = []
        self.species = {}
        self.reactions = []

    @abc.abstractmethod
    def add_rxd_func(self, sec):
        raise NotImplementedError

    def _add(self, name, diam, l, nseg=1):
        sec = super()._add(name, diam, l, nseg)
        if self._rxd_func:
            region, specie, reaction = self._rxd_func(sec)
            self._extend_rxd_lists(region, specie, reaction)
        try:
            region, specie, reaction = self.add_rxd_func(sec)
            self._extend_rxd_lists(region, specie, reaction)
        except NotImplementedError:
            return

    def _extend_rxd_lists(self, region, specie, reaction):
        if not isinstance(region, list):
            region = [region]
        if not isinstance(specie, list):
            specie = [specie]
        if not isinstance(reaction, list):
            reaction = [reaction]
        self.regions.extend(region)
        for s in specie:
            self.species[s.name] = s
        self.reactions.extend(reaction)


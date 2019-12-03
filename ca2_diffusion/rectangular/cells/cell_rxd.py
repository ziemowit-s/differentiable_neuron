import abc
from ca2_diffusion.rectangular.cells.cell import Cell


class CellRxD(Cell):
    def __init__(self, name):
        super().__init__(name)

        self._is_rxd_set = False

    def add_sec(self, name, diam, l, nseg=1):
        if self._is_rxd_set:
            raise MemoryError("RxD has been called earlier, after which you can't change morphology")
        super().add_sec(name, diam, l, nseg)

    def add_rxd(self):
        if self._is_rxd_set:
            raise MemoryError("RxD has been called earlier, it can be called only once, after all morphology is set")
        self._is_rxd_set = True
        self._add_rxd()

    @abc.abstractmethod
    def _add_rxd(self):
        raise NotImplementedError()



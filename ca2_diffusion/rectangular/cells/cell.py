from neuron import h


class Cell:
    def __init__(self, name, mechanism=None):
        """
        spine_head->spine_neck->dendrite
        """
        self._name = name
        self.secs = []
        if isinstance(mechanism, list):
            self.mechanisms = mechanism
        else:
            self.mechanisms = []

    def _add(self, name, diam, l, nseg=1):
        sec = h.Section(name=name, cell=self)
        sec.L = l
        sec.diam = diam
        sec.nseg = nseg

        for m in self.mechanisms:
            sec.insert(m)
        return sec

    def add(self, name, diam, l, nseg):
        n = self._add(name, diam, l, nseg)
        self.secs.append(n)

    def __repr__(self):
        return "Cell[{}]".format(self._name)
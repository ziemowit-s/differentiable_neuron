from neuron import h


class Cell:
    def __init__(self, name, mechanism=None):
        """
        spine_head->spine_neck->dendrite
        """
        self._name = name
        self.secs = {}
        if isinstance(mechanism, list):
            self.mechanisms = mechanism
        else:
            self.mechanisms = []

    def add_sec(self, name, diam, l, nseg):
        sec = h.Section(name=name, cell=self)
        sec.L = l
        sec.diam = diam
        sec.nseg = nseg

        for m in self.mechanisms:
            sec.insert(m)
        self.secs[name] = sec

    def connect(self, fr, to, loc=1.0):
        """default: fr(0.0) -> to(1.0)"""
        fr = self.secs[fr]
        to = self.secs[to]
        fr.connect(to(loc))

    def __repr__(self):
        return "Cell[{}]".format(self._name)
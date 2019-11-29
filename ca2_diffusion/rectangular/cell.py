from neuron import h


class Cell:
    def __init__(self, name, mechanism=None):
        """
        spine_head->spine_neck->dendrite
        """
        self._name = name

        self.head = h.Section(name='head', cell=self)
        self.head.L = 1
        self.head.diam = 1
        self.head.nseg = 101

        if mechanism:
            self.head.insert(mechanism)

    def __repr__(self):
        return "Cell[{}]".format(self._name)
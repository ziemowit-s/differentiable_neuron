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
        self.head.nseg = 11

        self.neck = h.Section(name='neck', cell=self)
        self.neck.L = 0.5
        self.neck.diam = 0.1
        self.neck.nseg = 11

        self.dend = h.Section(name='dend', cell=self)
        self.dend.L = 11
        self.dend.diam = 10.0
        self.dend.nseg = 110

        if mechanism:
            self.head.insert(mechanism)
            self.neck.insert(mechanism)

        self.all = [self.dend, self.neck, self.head]

        self.head.connect(self.neck)
        self.neck.connect(self.dend(0.5))

    def __repr__(self):
        return "Cell[{}]".format(self._name)
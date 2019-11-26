from neuron import h, gui
import matplotlib.pyplot as plt
h.load_file('stdrun.hoc')


class Cell:
    def __init__(self, name):
        """
        spine_head->spine_neck->dendrite
        """
        self._name = name

        self.head = h.Section(name='head', cell=self)
        self.head.L = 0.5
        self.head.diam = 0.5
        self.head.nseg = 11

        self.neck = h.Section(name='neck', cell=self)
        self.neck.L = 0.5
        self.neck.diam = 0.5
        self.neck.nseg = 11

        self.dend = h.Section(name='dend', cell=self)
        self.dend.L = 11
        self.dend.diam = 1.0
        self.dend.nseg = 110

        self.head.insert('cadifusrect')
        self.neck.insert('cadifusrect')

        self.all = [self.dend, self.neck, self.head]

        self.head.connect(self.neck)
        self.neck.connect(self.dend(0.5))

    def __repr__(self):
        return "Cell[{}]".format(self._name)


if __name__ == '__main__':
    cell = Cell(name=0)
    """
    proc init() {
        finitialize(v_init)
        ca_cadifusrect[0](.5) = 1e-2
        L_cadifusrect = L
        cvode.re_init()
    }
    xopen("cadif.ses")
    tstop = .02
    """

    # inject ca2+ to the first shell of head(0.5)
    cell.head.ca_cadifusrect[0](0.5)

    print(cell.dend(0.5).area())
    h.topology()
    h.PlotShape(False).plot(plt)

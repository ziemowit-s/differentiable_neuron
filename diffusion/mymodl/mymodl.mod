
TITLE My test modl

NEURON {
	SUFFIX mymodl
	READ L, nseg
}

UNITS {
	(um) =	(micron)
}

ASSIGNED {
    diam (um)
    L (um)
    nseg (1)
}

STATE {
	my_diam (um)
	my_L (um)
	my_nseg (1)
}

BREAKPOINT {
	my_L = L
	my_diam = diam
	my_nseg = nseg
}

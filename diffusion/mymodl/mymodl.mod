
TITLE My test modl

NEURON {
	SUFFIX mymodl
}

UNITS {
	(um) =	(micron)
}

ASSIGNED {
    diam (um)
    L (um)
}

STATE {
	my_diam (um)
	my_L (um)
}

BREAKPOINT {
	my_L = L
	my_diam = diam
}
